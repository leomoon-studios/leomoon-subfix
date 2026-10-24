[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ApplicationPath,
    [ValidateSet("x64", "arm64")][string]$Architecture = "x64"
)

$ErrorActionPreference = "Stop"
$application = (Resolve-Path -LiteralPath $ApplicationPath).Path
$bytes = [System.IO.File]::ReadAllBytes($application)
if ([System.Text.Encoding]::ASCII.GetString($bytes, 0, 2) -ne "MZ") {
    throw "The application is not a PE executable"
}
$peOffset = [System.BitConverter]::ToInt32($bytes, 0x3c)
$machine = [System.BitConverter]::ToUInt16($bytes, $peOffset + 4)
$expectedMachine = if ($Architecture -eq "arm64") { 0xAA64 } else { 0x8664 }
if ($machine -ne $expectedMachine) {
    throw "The application is not $Architecture"
}

$dumpbin = Get-Command dumpbin.exe -ErrorAction SilentlyContinue
if (-not $dumpbin) { throw "dumpbin.exe is required to verify PE dependencies" }
$dependencies = & $dumpbin.Source /DEPENDENTS $application
if ($LASTEXITCODE -ne 0) { throw "dumpbin /DEPENDENTS failed" }
foreach ($forbidden in @("MSVCP100.DLL", "MSVCR100.DLL")) {
    if ($dependencies -match [regex]::Escape($forbidden)) {
        throw "The application imports obsolete Visual C++ 2010 runtime $forbidden"
    }
}
Write-Host "Verified PE architecture and dependencies for $application"
