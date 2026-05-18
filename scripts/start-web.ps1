$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
Write-Host "Starting web on http://localhost:3001 (leave this window open)" -ForegroundColor Cyan
npm run dev --workspace=apps/web
