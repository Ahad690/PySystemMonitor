"""
Configuration Settings for PySystemMonitor
"""

class Config:
    # Application Settings
    APP_NAME = "PySystemMonitor"
    VERSION = "1.0.0"
    
    # Monitoring Intervals (in seconds)
    CPU_UPDATE_INTERVAL = 1
    MEMORY_UPDATE_INTERVAL = 1
    DISK_UPDATE_INTERVAL = 5
    NETWORK_UPDATE_INTERVAL = 1
    PROCESS_UPDATE_INTERVAL = 2
    
    # Alert Thresholds
    CPU_THRESHOLD = 80          # Alert when CPU > 80%
    MEMORY_THRESHOLD = 85       # Alert when Memory > 85%
    DISK_THRESHOLD = 90         # Alert when Disk > 90%
    
    # Logging Settings
    LOG_ENABLED = True
    LOG_FILE = "logs/system_monitor.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5
    
    # Performance History
    HISTORY_LENGTH = 60         # Keep 60 data points
    
    # GUI Settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    REFRESH_RATE = 1000         # milliseconds
    
    # Export Settings
    EXPORT_FORMAT = "csv"       # csv, json, or both
    EXPORT_PATH = "exports/"