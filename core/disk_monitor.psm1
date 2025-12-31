Import-Module "$PSScriptRoot\..\utils\helpers.psm1"

function Get-DiskUsage {
    $drives = Get-PSDrive -PSProvider FileSystem
    $results = @()
    
    foreach ($d in $drives) {
        if ($d.Used -gt 0 -and $d.Free -gt 0) {
            $total = $d.Used + $d.Free
            $percent = 0
            if ($total -gt 0) {
                $percent = ($d.Used / $total) * 100
            }
            
            # Lab 11: Disk Quota / Warning
            $status = "OK"
            # Warn if free space < 10%
            if ($percent -gt 90) { $status = "LOW_SPACE" }
            
            $results += @{
                device = $d.Name
                total = Format-Bytes $total
                used = Format-Bytes $d.Used
                free = Format-Bytes $d.Free
                percent = [math]::Round($percent, 1)
                status = $status
            }
        }
    }
    return $results
}

function Get-DiskIo {
    # This is a bit expensive, so we might want to optimize or cache
    $read = (Get-Counter '\PhysicalDisk(_Total)\Disk Read Bytes/sec' -ErrorAction SilentlyContinue).CounterSamples.CookedValue
    $write = (Get-Counter '\PhysicalDisk(_Total)\Disk Write Bytes/sec' -ErrorAction SilentlyContinue).CounterSamples.CookedValue
    
    return @{
        read_rate = Format-Bytes $read
        write_rate = Format-Bytes $write
        read_bytes = $read
        write_bytes = $write
    }
}

Export-ModuleMember -Function Get-DiskUsage, Get-DiskIo
