Import-Module "$PSScriptRoot\..\utils\helpers.psm1"

$global:LogBuffer = @()

function Write-Log {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [ValidateSet("INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG")]
        [string]$Level = "INFO",
        
        [string]$Component = "System"
    )
    
    $timestamp = Get-Timestamp
    $line = "[$timestamp] [$Level] [$Component] $Message"
    
    # Add to in-memory buffer for UI
    $global:LogBuffer += @{
        Timestamp = $timestamp
        Level = $Level
        Component = $Component
        Message = $Message
    }
    
    # Keep buffer small
    if ($global:LogBuffer.Count -gt 100) {
        $global:LogBuffer = $global:LogBuffer[-100..-1]
    }
    
    # Write to File
    # (We assume $Config is available or passed, but for simplicity we rely on a known path or param)
    # Ideally, this should be configured via Initialize-Logger
    try {
        Add-Content -Path "logs/system_monitor.log" -Value $line -ErrorAction SilentlyContinue
    } catch {}
    
    # Write to Console if Critical
    if ($Level -eq "CRITICAL" -or $Level -eq "ERROR") {
        Write-Host $line -ForegroundColor Red
    }
}

function Get-LogHistory {
    return $global:LogBuffer
}

function Rotate-Logs {
    param([int]$DaysToKeep = 7)
    
    $logDir = "logs"
    if (Test-Path $logDir) {
        $cutoff = (Get-Date).AddDays(-$DaysToKeep)
        Get-ChildItem -Path $logDir -Filter "*.log" | Where-Object { $_.LastWriteTime -lt $cutoff } | Remove-Item -Force
    }
}

Export-ModuleMember -Function Write-Log, Get-LogHistory, Rotate-Logs
