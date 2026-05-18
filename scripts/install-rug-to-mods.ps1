# Copy latest SimForge rug output into The Sims 4 Mods and remove duplicate Flokati packages.
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$mods = Join-Path $env:USERPROFILE "Documents\Electronic Arts\The Sims 4\Mods"
$src = Get-ChildItem -Path (Join-Path $repo "data\outputs") -Recurse -Filter "rug_*.package" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $src) {
    Write-Error "No rug_*.package found under data\outputs. Create one in SimForge Studio first."
}

New-Item -ItemType Directory -Force -Path $mods | Out-Null
$dest = Join-Path $mods "SimForge_Flokati_Brain.package"
Copy-Item $src.FullName $dest -Force

Get-ChildItem $mods -Filter "*Flokati*.package" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -ne $dest } |
    ForEach-Object {
        Write-Host "Removing duplicate: $($_.Name)"
        Remove-Item $_.FullName -Force
    }

Get-ChildItem $mods -Filter "rug_*.package" -ErrorAction SilentlyContinue |
    ForEach-Object {
        Write-Host "Removing old output: $($_.Name)"
        Remove-Item $_.FullName -Force
    }

Write-Host "Installed: $dest"
Write-Host "Size: $((Get-Item $dest).Length) bytes (expect about 4-6 MB)"
Write-Host "Restart The Sims 4 completely, search Flokati in Build/Buy."
