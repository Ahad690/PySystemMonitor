Import-Module "$PSScriptRoot\..\utils\helpers.psm1"

class Alert {
    [string]$Severity
    [string]$Message
    [string]$Timestamp
    
    Alert([string]$sev, [string]$msg) {
        $this.Severity = $sev
        $this.Message = $msg
        $this.Timestamp = Get-Timestamp
    }
}

$global:ShortTermHistory = @()

function Get-Alerts {
    return $global:ShortTermHistory
}

function Add-Alert {
    param(
        [string]$Severity,
        [string]$Message
    )
    $alert = [Alert]::new($Severity, $Message)
    $global:ShortTermHistory = @($alert) + $global:ShortTermHistory
    if ($global:ShortTermHistory.Count -gt 50) {
        $global:ShortTermHistory = $global:ShortTermHistory[0..49]
    }
    return $alert
}

function Check-Thresholds {
    param(
        [hashtable]$Config,
        [double]$Cpu,
        [double]$Memory,
        [double]$Disk
    )
    
    if ($Cpu -gt $Config.Alerts.CpuUsagePercent) {
        Add-Alert "WARNING" "High CPU Usage: $Cpu%"
    }
    
    if ($Memory -gt $Config.Alerts.MemoryUsagePercent) {
        Add-Alert "WARNING" "High Memory Usage: $Memory%"
    }
    
    if ($Disk -gt $Config.Alerts.DiskUsagePercent) {
        Add-Alert "WARNING" "High Disk Usage: $Disk%"
    }
}

function Clear-Alerts {
    $global:ShortTermHistory = @()
}

Export-ModuleMember -Function Get-Alerts, Add-Alert, Check-Thresholds, Clear-Alerts
