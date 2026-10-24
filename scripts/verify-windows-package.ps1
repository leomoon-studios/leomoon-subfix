[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$StageDirectory,
    [Parameter(Mandatory = $true)][string]$InstallerPath,
    [Parameter(Mandatory = $true)][ValidatePattern('^\d+\.\d+\.\d+$')][string]$Version,
    [Parameter(Mandatory = $true)][ValidateSet("x64")][string]$Architecture
)

$ErrorActionPreference = "Stop"
$stage = (Resolve-Path -LiteralPath $StageDirectory).Path
$installer = (Resolve-Path -LiteralPath $InstallerPath).Path
$application = Join-Path $stage "LeoMoon SubFix.exe"

if (-not (Test-Path -LiteralPath $application -PathType Leaf)) {
    throw "Expected application executable was not found: $application"
}
if ((Split-Path -Leaf $installer) -ne "leomoon-subfix-$Version-windows-$Architecture-setup.exe") {
    throw "Installer filename does not match the requested version and architecture"
}

$forbiddenFiles = @("msvcp100.dll", "msvcr100.dll", "istask.dll")
foreach ($forbidden in $forbiddenFiles) {
    if (Get-ChildItem -LiteralPath $stage -Recurse -File -Filter $forbidden) {
        throw "Obsolete binary is present in the staged application: $forbidden"
    }
}

$bytes = [System.IO.File]::ReadAllBytes($application)
if ([System.Text.Encoding]::ASCII.GetString($bytes, 0, 2) -ne "MZ") {
    throw "The staged application is not a PE executable"
}
$peOffset = [System.BitConverter]::ToInt32($bytes, 0x3c)
$machine = [System.BitConverter]::ToUInt16($bytes, $peOffset + 4)
if ($Architecture -eq "x64" -and $machine -ne 0x8664) {
    throw "The staged application is not x64"
}

$dumpbin = Get-Command dumpbin.exe -ErrorAction SilentlyContinue
if (-not $dumpbin) {
    throw "dumpbin.exe is required to verify PE dependencies"
}
$peBinaries = Get-ChildItem -LiteralPath $stage -Recurse -File |
    Where-Object { $_.Extension -in ".exe", ".dll", ".pyd" } |
    Where-Object {
        $candidateBytes = [System.IO.File]::ReadAllBytes($_.FullName)
        $candidateBytes.Length -ge 2 -and [System.Text.Encoding]::ASCII.GetString($candidateBytes, 0, 2) -eq "MZ"
    }
foreach ($binary in $peBinaries) {
    $dependencies = & $dumpbin.Source /DEPENDENTS $binary.FullName
    if ($LASTEXITCODE -ne 0) {
        throw "dumpbin /DEPENDENTS failed for $($binary.FullName)"
    }
    foreach ($forbidden in @("MSVCP100.DLL", "MSVCR100.DLL")) {
        if ($dependencies -match [regex]::Escape($forbidden)) {
            throw "$($binary.FullName) imports obsolete Visual C++ 2010 runtime $forbidden"
        }
    }
}

Write-Host "Verified $installer"
