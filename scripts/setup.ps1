# ContentCreator4Sims local setup (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "Installing npm dependencies..." -ForegroundColor Cyan
npm install

Write-Host "Installing Python worker dependencies..." -ForegroundColor Cyan
python -m pip install -r services/worker/requirements.txt

Write-Host "Generating dev template packages..." -ForegroundColor Cyan
python scripts/generate_dev_templates.py

Write-Host "Building Blender scenes (if Blender installed)..." -ForegroundColor Cyan
python blender/scripts/build_scenes.py

Write-Host ""
Write-Host "Done. Start the stack:" -ForegroundColor Green
Write-Host "  npm run dev:worker   # port 8000"
Write-Host "  npm run dev          # port 3000"
