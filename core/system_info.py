"""
System Information Module
Retrieves basic system and hardware information
"""

import psutil
import platform
import socket
from datetime import datetime

class SystemInfo:
    """Collect and provide system information"""
    
    def __init__(self):
        self.update()
    
    def update(self):
        """Update system information"""
        self._collect_os_info()
        self._collect_hardware_info()
        self._collect_network_info()
    
    def _collect_os_info(self):
        """Collect OS information"""
        self.os_name = platform.system()
        self.os_version = platform.version()
        self.os_release = platform.release()
        self.architecture = platform.machine()
        self.hostname = socket.gethostname()
        self.python_version = platform.python_version()
    
    def _collect_hardware_info(self):
        """Collect hardware information"""
        self.cpu_count_physical = psutil.cpu_count(logical=False)
        self.cpu_count_logical = psutil.cpu_count(logical=True)
        self.cpu_freq = psutil.cpu_freq()
        
        mem = psutil.virtual_memory()
        self.total_memory = mem.total
        
        disk = psutil.disk_usage('/')
        self.total_disk = disk.total
        
        # Boot time
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
    
    def _collect_network_info(self):
        """Collect network information"""
        try:
            self.ip_address = socket.gethostbyname(socket.gethostname())
        except:
            self.ip_address = "Unable to determine"
        
        self.network_interfaces = []
        for interface, addresses in psutil.net_if_addrs().items():
            self.network_interfaces.append(interface)
    
    def get_uptime(self) -> str:
        """Get system uptime"""
        uptime_seconds = (datetime.now() - self.boot_time).total_seconds()
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{days}d {hours}h {minutes}m"
    
    def get_summary(self) -> dict:
        """Get summary of system information"""
        return {
            "os": f"{self.os_name} {self.os_release}",
            "hostname": self.hostname,
            "architecture": self.architecture,
            "cpu_cores": f"{self.cpu_count_physical} physical, {self.cpu_count_logical} logical",
            "total_memory": self.total_memory,
            "total_disk": self.total_disk,
            "uptime": self.get_uptime(),
            "ip_address": self.ip_address
        }
    
    def __str__(self):
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                     SYSTEM INFORMATION                        ║
╠══════════════════════════════════════════════════════════════╣
║  OS: {self.os_name} {self.os_release:<47}║
║  Hostname: {self.hostname:<50}║
║  Architecture: {self.architecture:<46}║
║  CPU Cores: {self.cpu_count_physical} physical, {self.cpu_count_logical} logical{' '*30}║
║  Uptime: {self.get_uptime():<52}║
║  IP Address: {self.ip_address:<48}║
╚══════════════════════════════════════════════════════════════╝
"""