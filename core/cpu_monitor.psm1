function Get-CpuUsage {
    $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -ErrorAction SilentlyContinue
    if ($cpu) {
        return [math]::Round($cpu.CounterSamples.CookedValue, 1)
    }
    return 0
}

function Get-CpuInfo {
    $proc = Get-CimInstance Win32_Processor | Select-Object -First 1
    return @{
        Name = $proc.Name
        Cores = $proc.NumberOfCores
        Threads = $proc.NumberOfLogicalProcessors
    }
}

Export-ModuleMember -Function Get-CpuUsage, Get-CpuInfo
