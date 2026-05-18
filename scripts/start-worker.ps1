$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..\services\worker")
Write-Host "Starting worker on http://127.0.0.1:8000 (leave this window open)" -ForegroundColor Cyan
python -m app
