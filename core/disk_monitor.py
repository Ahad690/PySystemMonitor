"""
Disk Monitoring Module
Monitors disk usage and I/O operations
"""

import psutil
import time
from typing import Dict, List
from config.settings import Config
from utils.helpers import bytes_to_human_readable

class DiskMonitor:
    """Monitor disk usage and I/O"""
    
    def __init__(self):
        self.partitions = []
        self.disk_usage = {}
        self.io_counters = {}
        self.previous_io = None
        self.io_rates = {"read": 0, "write": 0}
        self._last_update = 0
    
    def update(self) -> Dict:
        """Update disk statistics"""
        # Get partitions
        self.partitions = []
        for partition in psutil.disk_partitions():
            try:
                partition_info = {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts
                }
                
                # Get usage for this partition
                usage = psutil.disk_usage(partition.mountpoint)
                partition_info.update({
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                })
                
                self.partitions.append(partition_info)
            except (PermissionError, OSError):
                pass
        
        # Get I/O counters
        current_io = psutil.disk_io_counters()
        current_time = time.time()
        
        if self.previous_io and self._last_update:
            time_delta = current_time - self._last_update
            if time_delta > 0:
                self.io_rates = {
                    "read": (current_io.read_bytes - self.previous_io.read_bytes) / time_delta,
                    "write": (current_io.write_bytes - self.previous_io.write_bytes) / time_delta
                }
        
        self.previous_io = current_io
        self._last_update = current_time
        
        self.io_counters = {
            "read_count": current_io.read_count,
            "write_count": current_io.write_count,
            "read_bytes": current_io.read_bytes,
            "write_bytes": current_io.write_bytes,
            "read_time": current_io.read_time,
            "write_time": current_io.write_time
        }
        
        return self.disk_usage
    
    def get_partitions(self) -> List[Dict]:
        """Get all disk partitions with usage"""
        return self.partitions
    
    def get_io_counters(self) -> Dict:
        """Get disk I/O counters"""
        return self.io_counters
    
    def get_io_rates(self) -> Dict:
        """Get current I/O rates (bytes/second)"""
        return {
            "read_rate": bytes_to_human_readable(self.io_rates["read"]) + "/s",
            "write_rate": bytes_to_human_readable(self.io_rates["write"]) + "/s"
        }
    
    def get_total_usage(self) -> Dict:
        """Get total disk usage across all partitions"""
        total = 0
        used = 0
        
        for partition in self.partitions:
            total += partition.get("total", 0)
            used += partition.get("used", 0)
        
        percent = (used / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "used": used,
            "free": total - used,
            "percent": percent
        }
    
    def is_high_usage(self, threshold: float = Config.DISK_THRESHOLD) -> bool:
        """Check if any disk is above threshold"""
        for partition in self.partitions:
            if partition.get("percent", 0) > threshold:
                return True
        return False
    
    def get_partition_summary(self) -> List[Dict]:
        """Get human-readable partition summary"""
        summary = []
        for p in self.partitions:
            summary.append({
                "device": p["device"],
                "mountpoint": p["mountpoint"],
                "total": bytes_to_human_readable(p.get("total", 0)),
                "used": bytes_to_human_readable(p.get("used", 0)),
                "free": bytes_to_human_readable(p.get("free", 0)),
                "percent": f"{p.get('percent', 0):.1f}%"
            })
        return summary
    
    def get_stats(self) -> Dict:
        """Get comprehensive disk statistics"""
        return {
            "partitions": self.get_partition_summary(),
            "io_counters": self.io_counters,
            "io_rates": self.get_io_rates(),
            "total_usage": self.get_total_usage()
        }
    
    def __str__(self):
        output = "\nDisk Statistics:\n"
        for p in self.get_partition_summary():
            output += f"  {p['device']} ({p['mountpoint']}): "
            output += f"{p['used']} / {p['total']} ({p['percent']})\n"
        rates = self.get_io_rates()
        output += f"  I/O Rates: Read {rates['read_rate']}, Write {rates['write_rate']}\n"
        return output