Import-Module "$PSScriptRoot\..\utils\helpers.psm1"

function Get-MemoryUsage {
    $os = Get-CimInstance Win32_OperatingSystem
    $total = $os.TotalVisibleMemorySize * 1KB
    $free = $os.FreePhysicalMemory * 1KB
    $used = $total - $free
    $percent = ($used / $total) * 100
    
    return @{
        total = Format-Bytes $total
        used = Format-Bytes $used
        free = Format-Bytes $free
        percent = [math]::Round($percent, 1)
        total_bytes = $total
    }
}

Export-ModuleMember -Function Get-MemoryUsage
