@{
    AppName = "PySystemMonitor-PS"
    Version = "2.0.0"
    UpdateInterval = 1000 # milliseconds
    
    # Alert Thresholds
    Alerts = @{
        CpuUsagePercent = 85
        MemoryUsagePercent = 90
        DiskUsagePercent = 90
    }
    
    # Logging & Automation (Lab 5)
    LogPath = "logs/system_monitor.log"
    DataExportPath = "dashboard/data.js"
    LogRotationDays = 7
    SnapshotInterval = 300
    
    # Diagnostics (Lab 6)
    CriticalServices = @('wuauserv', 'EventLog', 'Spooler', 'Dnscache')
    EventLogQueryHours = 24
    
    # Security (Lab 10)
    FailedLoginThreshold = 5
    ComplianceCheckInterval = 3600
    
    # Advanced Ops (Lab 11)
    LargeFileSizeMB = 500
    DiskAlertThresholdGB = 5
    
    # Agentic & Workflows (Lab 8)
    DefaultPriority = "Medium"
    WorkflowCheckpoints = $true
}
