# Stop Node (Next.js) and Python worker on ports 3001 and 8000
foreach ($port in 3001, 8000) {
    $lines = netstat -ano | Select-String ":$port\s"
    foreach ($line in $lines) {
        if ($line -match '\s+(\d+)\s*$') {
            $procId = $Matches[1]
            if ($procId -ne "0") {
                Write-Host "Stopping PID $procId on port $port"
                taskkill /PID $procId /F 2>$null
            }
        }
    }
}
Write-Host "Done. You can run start-worker.ps1 and start-web.ps1 in two terminals." -ForegroundColor Green
