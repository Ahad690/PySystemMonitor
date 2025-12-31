function Get-TopProcesses {
    param(
        [int]$Count = 10
    )
    
    $procs = Get-Process | Sort-Object CPU -Descending | Select-Object -First $Count
    $results = @()
    
    foreach ($p in $procs) {
        $cpu = if ($p.CPU) { $p.CPU } else { 0 }
        # Approximation of CPU % usage (not perfect in PS without tracking time)
        # For now, we return raw CPU time or a placeholder. 
        # Better: use Win32_PerfFormattedData_PerfProc_Process but that's slow.
        # We will return the CPU time as a metric for sorting.
        
        $results += @{
            pid = $p.Id
            name = $p.Name
            cpu_percent = $cpu # This is actually CPU *Time* in seconds, interpreting as "score"
            memory_percent = [math]::Round(($p.WS / (Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize) * 100 / 1KB, 1)
            status = if ($p.Responding) { "Running" } else { "Not Resp" }
        }
    }
    return $results
}

function Stop-ProcessById {
    param(
        [int]$Id
    )
    
    try {
        Stop-Process -Id $Id -Force -ErrorAction Stop
        return @{ success = $true; message = "Process $Id terminated." }
    }
    catch {
        return @{ success = $false; message = "Error: $($_.Exception.Message)" }
    }
}

Export-ModuleMember -Function Get-TopProcesses, Stop-ProcessById
