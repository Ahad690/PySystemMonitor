function Format-Bar {
    param(
        [double]$Percent,
        [int]$Width = 40
    )
    
    $filled = [int]($Width * $Percent / 100)
    $empty = $Width - $filled
    if ($empty -lt 0) { $empty = 0 }
    
    $color = "Green"
    if ($Percent -gt 80) { $color = "Red" }
    elseif ($Percent -gt 50) { $color = "Yellow" }
    
    $bar = "█" * $filled + "░" * $empty
    
    Write-Host "  [$bar] " -NoNewline -ForegroundColor $color
    Write-Host ("{0,5:N1}%" -f $Percent) -NoNewline
}

function Show-Dashboard {
    param(
        $MonitorData
    )
    
    Clear-Host
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host "                    PySystemMonitor-PS v1.0" -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host "  Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host ("=" * 70) -ForegroundColor Cyan
    
    Write-Host "`n┌─ SYSTEM OVERVIEW ─────────────────────────────────────────────────┐"
    
    Write-Host "  CPU:    " -NoNewline
    Format-Bar $MonitorData.Cpu.Current
    Write-Host ""
    
    Write-Host "  Memory: " -NoNewline
    Format-Bar $MonitorData.Memory.percent
    Write-Host ""
    
    Write-Host "  Network: Up $($MonitorData.Network.upload) Down $($MonitorData.Network.download)"
    Write-Host "  Disk:    R $($MonitorData.DiskIo.read_rate) W $($MonitorData.DiskIo.write_rate)"
    
    Write-Host "└───────────────────────────────────────────────────────────────────┘"
    
    Write-Host "`n┌─ TOP PROCESSES ───────────────────────────────────────────────────┐"
    Write-Host "  PID      NAME                          CPU     MEM%    STATUS" -ForegroundColor Gray
    foreach ($p in $MonitorData.Processes) {
        $cpuStr = "{0:N1}" -f $p.cpu_percent
        $memStr = "{0:N1}" -f $p.memory_percent
        Write-Host ("  {0,-8} {1,-30} {2,-7} {3,-7} {4,-8}" -f $p.pid, $p.name, $cpuStr, $memStr, $p.status)
    }
    Write-Host "└───────────────────────────────────────────────────────────────────┘"
    
    if ($MonitorData.Alerts.Count -gt 0) {
        Write-Host "`n┌─ RECENT ALERTS ───────────────────────────────────────────────────┐"
        foreach ($a in $MonitorData.Alerts[0..([math]::Min($MonitorData.Alerts.Count, 4))]) {
            if ($a) {
                $color = if ($a.Severity -eq "CRITICAL") { "Red" } else { "Yellow" }
                Write-Host "  [$($a.Severity)] $($a.Message)" -ForegroundColor $color
            }
        }
        Write-Host "└───────────────────────────────────────────────────────────────────┘"
    }
    
    Write-Host "`n[Q] Quit  [K] Kill Process  [R] Refresh" -ForegroundColor Cyan
}

Export-ModuleMember -Function Show-Dashboard
