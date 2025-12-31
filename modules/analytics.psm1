function Get-HealthScore {
    param(
        [double]$Cpu,
        [double]$Memory,
        [int]$AlertCount
    )
    
    $score = 100
    
    if ($Cpu -gt 80) { $score -= 20 }
    elseif ($Cpu -gt 60) { $score -= 10 }
    
    if ($Memory -gt 90) { $score -= 20 }
    elseif ($Memory -gt 70) { $score -= 10 }
    
    $score -= ($AlertCount * 5)
    
    if ($score -lt 0) { $score = 0 }
    
    $status = "Good"
    if ($score -lt 50) { $status = "Critical" }
    elseif ($score -lt 80) { $status = "Warning" }
    
    return @{
        score = $score
        status = $status
    }
}

Export-ModuleMember -Function Get-HealthScore
