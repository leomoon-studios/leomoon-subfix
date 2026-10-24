[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ArtifactDirectory,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
    [ValidateSet("x64")][string]$Architecture = "x64"
)

$ErrorActionPreference = "Stop"
$repoDirectory = Split-Path -Parent $PSScriptRoot
$artifacts = (Resolve-Path -LiteralPath $ArtifactDirectory).Path
$installer = Join-Path $artifacts "leomoon-subfix-$Version-windows-$Architecture-setup.exe"
$checksums = Join-Path $artifacts "SHA256SUMS"
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) { throw "Windows installer is missing" }
if (-not (Test-Path -LiteralPath $checksums -PathType Leaf)) { throw "SHA256SUMS is missing" }

foreach ($line in Get-Content -LiteralPath $checksums) {
    if ($line -notmatch '^([0-9a-f]{64}) \*(.+)$') { throw "Invalid SHA256SUMS entry: $line" }
    $actual = (Get-FileHash -LiteralPath (Join-Path $artifacts $Matches[2]) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $Matches[1]) { throw "Checksum mismatch for $($Matches[2])" }
}

function Invoke-CheckedProcess([string]$FilePath, [string[]]$Arguments, [int]$TimeoutSeconds = 60) {
    $process = Start-Process -FilePath $FilePath -ArgumentList $Arguments -PassThru
    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
        $process.Kill($true)
        throw "$FilePath did not finish within $TimeoutSeconds seconds"
    }
    if ($process.ExitCode -ne 0) { throw "$FilePath failed with exit code $($process.ExitCode)" }
}

$testRoot = Join-Path $env:RUNNER_TEMP "leomoon-subfix-windows-installer-smoke"
$installDirectory = Join-Path $testRoot "application"
$installLog = Join-Path $env:RUNNER_TEMP "leomoon-subfix-install.log"
$uninstallLog = Join-Path $env:RUNNER_TEMP "leomoon-subfix-uninstall.log"
try {
    Remove-Item -LiteralPath $testRoot -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    $installArguments = @("/SP-", "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/LOG=`"$installLog`"", "/DIR=`"$installDirectory`"")
    Invoke-CheckedProcess $installer $installArguments 600
    $application = Join-Path $installDirectory "LeoMoon SubFix.exe"
    if (-not (Test-Path -LiteralPath $application -PathType Leaf)) { throw "Installed application is missing" }
    if (Get-ChildItem -LiteralPath $installDirectory -Recurse -File -Include msvcp100.dll,msvcr100.dll,istask.dll) { throw "Installer deployed an obsolete binary" }

    $fixture = Join-Path $testRoot "legacy-windows-1256.srt"
    Copy-Item -LiteralPath (Join-Path $repoDirectory "tests\fixtures\legacy-windows-1256.srt") -Destination $fixture
    Invoke-CheckedProcess $application @("--convert", $fixture)
    if (-not (Test-Path -LiteralPath (Join-Path $testRoot "legacy-windows-1256_fixed.srt") -PathType Leaf)) { throw "Installed application did not convert the fixture" }

    Invoke-CheckedProcess $installer $installArguments 600
    $uninstaller = Join-Path $installDirectory "unins000.exe"
    if (-not (Test-Path -LiteralPath $uninstaller -PathType Leaf)) { throw "Windows uninstaller is missing" }
    Invoke-CheckedProcess $uninstaller @("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/LOG=`"$uninstallLog`"") 600
    if (Test-Path -LiteralPath $installDirectory) { throw "Application directory remains after uninstall" }
} finally {
    Remove-Item -LiteralPath $testRoot -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Windows installer install, conversion, upgrade, and uninstall checks passed"
