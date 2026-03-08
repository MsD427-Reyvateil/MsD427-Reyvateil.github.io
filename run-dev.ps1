# Run Hugo dev server. Use: .\run-dev.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$hugoExe = Join-Path $PSScriptRoot "hugo\hugo.exe"
if (-not (Test-Path $hugoExe)) {
    Write-Host "hugo\hugo.exe not found. Install Hugo Extended and add to PATH, or download to hugo\ folder." -ForegroundColor Yellow
    hugo version
    hugo server --disableFastRender
} else {
    & $hugoExe server --disableFastRender
}
