# PySystemMonitor-PS
# Main Entry Point

$ScriptRoot = $PSScriptRoot

# Import Configuration
$Config = Import-PowerShellDataFile "$ScriptRoot\config\settings.psd1"

# Import Core Modules
Import-Module "$ScriptRoot\core\cpu_monitor.psm1"
Import-Module "$ScriptRoot\core\memory_monitor.psm1"
Import-Module "$ScriptRoot\core\disk_monitor.psm1"
Import-Module "$ScriptRoot\core\network_monitor.psm1"
Import-Module "$ScriptRoot\core\process_manager.psm1"
Import-Module "$ScriptRoot\core\system_info.psm1"
Import-Module "$ScriptRoot\core\automation_framework.psm1"
Import-Module "$ScriptRoot\core\event_log_analyzer.psm1"
Import-Module "$ScriptRoot\core\service_monitor.psm1"
Import-Module "$ScriptRoot\core\environment_manager.psm1"

# Import Interface & Modules
Import-Module "$ScriptRoot\interfaces\cli.psm1"
Import-Module "$ScriptRoot\modules\alert_system.psm1"
Import-Module "$ScriptRoot\modules\logger.psm1"
Import-Module "$ScriptRoot\modules\analytics.psm1"
Import-Module "$ScriptRoot\modules\centralized_logger.psm1"
Import-Module "$ScriptRoot\modules\job_scheduler.psm1"
Import-Module "$ScriptRoot\modules\agentic_engine.psm1"
Import-Module "$ScriptRoot\security\security_monitor.psm1"

$Running = $true
$UpdateInterval = $Config.UpdateInterval / 1000

Write-Host "Initializing PySystemMonitor-PS Enterprise Edition..."
Start-Sleep -Seconds 1

# Cache for heavy operations (Lab 7 - Simple Caching Approach)
$CacheInterval = 10 # Refresh heavy data every 10 seconds
$LastCacheUpdate = [DateTime]::MinValue
$CachedSecurityAlerts = @()
$CachedServices = @()

# Ensure dashboard directory
$WebDataPath = "$ScriptRoot\$($Config.DataExportPath)"
$WebDir = Split-Path $WebDataPath
if (-not (Test-Path $WebDir)) {
    New-Item -ItemType Directory -Path $WebDir -Force | Out-Null
}

try {
    while ($Running) {
        $now = Get-Date
        
        # Update cache if needed (every 10 seconds)
        if (($now - $LastCacheUpdate).TotalSeconds -ge $CacheInterval) {
            Write-Host "Refreshing security and service data..." -ForegroundColor Gray
            $CachedSecurityAlerts = Get-SecurityAlerts -FailedLoginThreshold $Config.FailedLoginThreshold
            $CachedServices = Get-CriticalServices -ServiceNames $Config.CriticalServices
            $LastCacheUpdate = $now
        }
        
        # 1. Collect Base Data (Fast)
        $cpu = Get-CpuUsage
        $mem = Get-MemoryUsage
        $disk = Get-DiskUsage
        $diskIo = Get-DiskIo
        $net = Get-NetworkStats
        $procs = Get-TopProcesses -Count 5
        
        # 2. Use Cached Advanced Data
        $secAlerts = $CachedSecurityAlerts
        $services = $CachedServices
        
        # 3. Agentic Insights (Lab 8)
        $currentState = @{ Cpu = @{ Current = $cpu }; Disk = $disk; Alerts = $secAlerts }
        $insights = Get-NextBestAction -SystemState $currentState
        
        # 4. Check Thresholds
        Check-Thresholds -Config $Config -Cpu $cpu -Memory $mem.percent -Disk $disk[0].percent
        $alerts = Get-Alerts
       
        # Combine security alerts with system alerts
        if ($secAlerts -and $secAlerts.Count -gt 0) { 
            foreach ($sa in $secAlerts) {
                $alerts += $sa
            }
        }
        
        # 5. Analytics
        $health = Get-HealthScore -Cpu $cpu -Memory $mem.percent -AlertCount $alerts.Count
        
        # 6. Compile State
        $state = @{
            Cpu = @{ Current = $cpu }
            Memory = $mem
            Disk = $disk
            DiskIo = $diskIo
            Network = $net
            Processes = $procs
            Alerts = $alerts
            Health = $health
            Timestamp = Get-Date -Format "HH:mm:ss"
            
            # Enterprise Modules
            Services = $services
            Insights = $insights
        }
        
        # 7. Update Web Data
        Export-To-Web -Path $WebDataPath -Data $state
        
        # 8. Update CLI
        Show-Dashboard -MonitorData $state
        
        # 9. Handle Input
        if ([Console]::KeyAvailable) {
            $key = [Console]::ReadKey($true)
            switch ($key.Key) {
                "Q" { $Running = $false }
                "R" { continue }
                "K" {
                    $pidToKill = Read-Host "Enter PID to kill"
                    if ($pidToKill) {
                        try {
                            Stop-Process -Id $pidToKill -Force -ErrorAction Stop
                            Write-Host "Process $pidToKill terminated." -ForegroundColor Yellow
                        } catch {
                            Write-Host "Failed to kill process: $_" -ForegroundColor Red
                        }
                        Start-Sleep -Seconds 2
                    }
                }
            }
        }
        
        Start-Sleep -Seconds $UpdateInterval
    }
}
catch {
    Write-Host "Fatal Error: $_" -ForegroundColor Red
}
finally {
    Write-Host "`nStopping PySystemMonitor-PS..."
}
