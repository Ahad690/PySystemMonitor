function Format-Bytes {
    param (
        [double]$Bytes
    )
    
    $units = @("B", "KB", "MB", "GB", "TB", "PB")
    $i = 0
    while ($Bytes -ge 1024 -and $i -lt $units.Count - 1) {
        $Bytes /= 1024
        $i++
    }
    
    return "{0:N2} {1}" -f $Bytes, $units[$i]
}

function Get-Timestamp {
    return Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

Export-ModuleMember -Function Format-Bytes, Get-Timestamp
