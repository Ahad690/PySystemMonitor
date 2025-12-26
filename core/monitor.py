"""
System Monitor Aggregator
Central class that manages all monitoring components
"""

import threading
from core.cpu_monitor import CPUMonitor
from core.memory_monitor import MemoryMonitor
from core.disk_monitor import DiskMonitor
from core.network_monitor import NetworkMonitor
from core.process_manager import ProcessManager
from core.system_info import SystemInfo
from modules.alert_system import AlertSystem
from modules.logger import SystemLogger
from modules.analytics import PerformanceAnalytics

class SystemMonitor:
    """
    Central system monitoring class that coordinates all sub-monitors
    """
    
    def __init__(self):
        # Initialize Logger first
        self.logger = SystemLogger()
        self.logger.info("Initializing PySystemMonitor...")
        
        # Initialize Core Monitors
        self.system_info = SystemInfo()
        self.cpu_monitor = CPUMonitor()
        self.memory_monitor = MemoryMonitor()
        self.disk_monitor = DiskMonitor()
        self.network_monitor = NetworkMonitor()
        self.process_manager = ProcessManager()
        
        # Initialize Modules
        self.alert_system = AlertSystem()
        self.analytics = PerformanceAnalytics()
        
        # Connect Alerts
        self.alert_system.add_callback(self.logger.log_alert)
        
        self.logger.info("System Monitor initialized successfully")
        
    def update_all(self):
        """Update all monitors"""
        # Update core metrics
        cpu_usage = self.cpu_monitor.update()
        mem_info = self.memory_monitor.update()
        disk_info = self.disk_monitor.update()
        net_info = self.network_monitor.update()
        
        # Update analytics
        self.analytics.add_data_point(
            cpu=cpu_usage,
            memory=mem_info.get("percent", 0),
            disk_io=0, # Simplified
            network=0  # Simplified
        )
        
        # Check for alerts
        self.alert_system.check_cpu(cpu_usage)
        self.alert_system.check_memory(mem_info.get("percent", 0))
        self.alert_system.check_disk(self.disk_monitor.get_total_usage().get("percent", 0))
        
        # Log performance occasionally (could be optimized)
        # self.logger.log_performance({...})
        
    def get_summary(self):
        """Get a summary of current system state"""
        return {
            "cpu": self.cpu_monitor.get_stats(),
            "memory": self.memory_monitor.get_stats(),
            "disk": self.disk_monitor.get_stats(),
            "network": self.network_monitor.get_stats(),
            "alerts": len(self.alert_system.get_active_alerts())
        }
