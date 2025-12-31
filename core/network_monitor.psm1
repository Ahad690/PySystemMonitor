Import-Module "$PSScriptRoot\..\utils\helpers.psm1"

$global:LastNetStats = @{}
$global:LastNetTime = Get-Date

function Get-NetworkStats {
    $stats = Get-NetAdapterStatistics | Where-Object { $_.ReceivedBytes -gt 0 -or $_.SentBytes -gt 0 }
    
    $totalRx = ($stats | Measure-Object -Property ReceivedBytes -Sum).Sum
    $totalTx = ($stats | Measure-Object -Property SentBytes -Sum).Sum
    
    $now = Get-Date
    $timeDiff = ($now - $global:LastNetTime).TotalSeconds
    
    if ($timeDiff -eq 0) { $timeDiff = 1 }
    
    $rxRate = 0
    $txRate = 0
    
    if ($global:LastNetStats.Count -gt 0) {
        $rxRate = ($totalRx - $global:LastNetStats.TotalRx) / $timeDiff
        $txRate = ($totalTx - $global:LastNetStats.TotalTx) / $timeDiff
    }
    
    # Store current values for next calculation
    $global:LastNetStats = @{
        TotalRx = $totalRx
        TotalTx = $totalTx
    }
    $global:LastNetTime = $now
    
    if ($rxRate -lt 0) { $rxRate = 0 }
    if ($txRate -lt 0) { $txRate = 0 }
    
    return @{
        upload = Format-Bytes $txRate
        download = Format-Bytes $rxRate
        upload_bytes = $txRate
        download_bytes = $rxRate
    }
}

Export-ModuleMember -Function Get-NetworkStats
