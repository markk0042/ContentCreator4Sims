# Download Microsoft texconv.exe (DirectXTex) into tools/texconv/
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$DestDir = Join-Path $Root "tools\texconv"
$Dest = Join-Path $DestDir "texconv.exe"
$Url = "https://github.com/microsoft/DirectXTex/releases/download/oct2024/texconv.exe"

New-Item -ItemType Directory -Force -Path $DestDir | Out-Null

if (Test-Path $Dest) {
    Write-Host "Already installed: $Dest" -ForegroundColor Green
    exit 0
}

Write-Host "Downloading texconv.exe from DirectXTex..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $Url -OutFile $Dest -UseBasicParsing

Write-Host "Installed: $Dest" -ForegroundColor Green
Write-Host "Restart the worker (npm run dev:worker), then try the rug again." -ForegroundColor Yellow
