[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$StageDirectory,
    [Parameter(Mandatory = $true)][string]$DistDirectory,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d{4}-\d{2}-\d{2}T')][string]$ReleaseDate,
    [Parameter(Mandatory = $true)][ValidatePattern('^[0-9a-fA-F]{7,64}$')][string]$Commit,
    [ValidateSet("x64")][string]$Architecture = "x64",
    [string]$IsccPath = ""
)

$ErrorActionPreference = "Stop"
$repoDirectory = Split-Path -Parent $PSScriptRoot
$sourceStage = (Resolve-Path -LiteralPath $StageDirectory).Path
if (-not (Test-Path -LiteralPath (Join-Path $sourceStage "LeoMoon SubFix.exe") -PathType Leaf)) {
    throw "StageDirectory must contain LeoMoon SubFix.exe"
}

if (-not $IsccPath) {
    $command = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($command) {
        $IsccPath = $command.Source
    } else {
        $IsccPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    }
}
if (-not (Test-Path -LiteralPath $IsccPath -PathType Leaf)) {
    throw "Inno Setup compiler was not found at $IsccPath"
}

$packageDirectory = Join-Path $repoDirectory "build\package\windows"
$stage = Join-Path $packageDirectory "stage"
$installerScript = Join-Path $repoDirectory "packaging\windows\subfix.iss"
$license = Join-Path $repoDirectory "LICENSE"
Remove-Item -LiteralPath $packageDirectory -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $stage -Force | Out-Null
Copy-Item -Path (Join-Path $sourceStage "*") -Destination $stage -Recurse -Force
New-Item -ItemType Directory -Path (Join-Path $stage "licenses") -Force | Out-Null
Copy-Item -LiteralPath $license -Destination (Join-Path $stage "licenses\LICENSE")
Copy-Item -LiteralPath (Join-Path $repoDirectory "THIRD_PARTY_NOTICES.md") -Destination (Join-Path $stage "licenses\THIRD_PARTY_NOTICES.md")

$certificatePath = $env:SUBFIX_WINDOWS_CERTIFICATE_PATH
$certificatePassword = $env:SUBFIX_WINDOWS_CERTIFICATE_PASSWORD
$timestampUrl = $env:SUBFIX_WINDOWS_TIMESTAMP_URL
if (-not $timestampUrl) { $timestampUrl = "http://timestamp.digicert.com" }

function Get-SignTool {
    $kitsRoot = Join-Path ${env:ProgramFiles(x86)} "Windows Kits\10\bin"
    $tool = Get-ChildItem -LiteralPath $kitsRoot -Filter signtool.exe -File -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '\\x64\\signtool\.exe$' } |
        Sort-Object FullName -Descending |
        Select-Object -First 1
    if (-not $tool) { throw "signtool.exe was not found in the Windows SDK" }
    return $tool.FullName
}

function Sign-Artifact([string]$Path, [string]$SignTool) {
    $arguments = @("sign", "/fd", "SHA256", "/td", "SHA256", "/tr", $timestampUrl, "/f", $certificatePath)
    if ($certificatePassword) { $arguments += @("/p", $certificatePassword) }
    $arguments += $Path
    & $SignTool @arguments
    if ($LASTEXITCODE -ne 0) { throw "Authenticode signing failed for $Path" }
    if ((Get-AuthenticodeSignature -LiteralPath $Path).Status -ne "Valid") {
        throw "Authenticode signature validation failed for $Path"
    }
}

$signTool = $null
if ($certificatePath) {
    if (-not (Test-Path -LiteralPath $certificatePath -PathType Leaf)) { throw "Configured signing certificate does not exist" }
    $signTool = Get-SignTool
    Sign-Artifact (Join-Path $stage "LeoMoon SubFix.exe") $signTool
}

& $IsccPath "/Qp" "/DAppVersion=$Version" "/DStageDir=$stage" "/DOutputDir=$packageDirectory" "/DLicenseFile=$license" $installerScript
if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed with exit code $LASTEXITCODE" }
$installer = Join-Path $packageDirectory "leomoon-subfix-$Version-windows-$Architecture-setup.exe"
if ($signTool) { Sign-Artifact $installer $signTool }

& (Join-Path $PSScriptRoot "verify-windows-package.ps1") -StageDirectory $stage -InstallerPath $installer -Version $Version -Architecture $Architecture

$dist = [System.IO.Path]::GetFullPath($DistDirectory)
if ($dist -eq [System.IO.Path]::GetPathRoot($dist) -or $dist -eq $repoDirectory) { throw "Refusing to replace unsafe artifact directory: $dist" }
if (Test-Path -LiteralPath $dist) { Remove-Item -LiteralPath $dist -Recurse -Force }
New-Item -ItemType Directory -Path $dist | Out-Null
Copy-Item -LiteralPath $installer -Destination $dist

$manifest = [ordered]@{
    application = "LeoMoon SubFix"
    version = $Version
    releaseDate = $ReleaseDate
    commit = $Commit
    platform = "windows"
    architecture = $Architecture
    format = "Inno Setup"
    signed = [bool]$signTool
}
$manifest | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $dist "release-manifest.json") -Encoding utf8NoBOM
Get-ChildItem -LiteralPath $dist -File | Sort-Object Name | ForEach-Object {
    "{0} *{1}" -f (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant(), $_.Name
} | Set-Content -LiteralPath (Join-Path $dist "SHA256SUMS") -Encoding ascii

Write-Host "Windows release artifacts are ready in $dist"
