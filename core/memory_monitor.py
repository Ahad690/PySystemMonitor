"""
Memory Monitoring Module
Monitors RAM and Swap usage
"""

import psutil
from collections import deque
from typing import Dict, List
from config.settings import Config
from utils.helpers import bytes_to_human_readable

class MemoryMonitor:
    """Monitor memory (RAM and Swap) usage"""
    
    def __init__(self, history_length: int = Config.HISTORY_LENGTH):
        self.history_length = history_length
        self.ram_history = deque(maxlen=history_length)
        self.swap_history = deque(maxlen=history_length)
        
        self.current_ram = {}
        self.current_swap = {}
    
    def update(self) -> Dict:
        """Update memory statistics"""
        # RAM statistics
        ram = psutil.virtual_memory()
        self.current_ram = {
            "total": ram.total,
            "available": ram.available,
            "used": ram.used,
            "free": ram.free,
            "percent": ram.percent,
            "cached": getattr(ram, 'cached', 0),
            "buffers": getattr(ram, 'buffers', 0)
        }
        self.ram_history.append(ram.percent)
        
        # Swap statistics
        swap = psutil.swap_memory()
        self.current_swap = {
            "total": swap.total,
            "used": swap.used,
            "free": swap.free,
            "percent": swap.percent
        }
        self.swap_history.append(swap.percent)
        
        return self.current_ram
    
    def get_ram_usage(self) -> Dict:
        """Get current RAM usage"""
        return self.current_ram
    
    def get_swap_usage(self) -> Dict:
        """Get current Swap usage"""
        return self.current_swap
    
    def get_ram_percent(self) -> float:
        """Get RAM usage percentage"""
        return self.current_ram.get("percent", 0)
    
    def get_ram_history(self) -> List[float]:
        """Get RAM usage history"""
        return list(self.ram_history)
    
    def get_swap_history(self) -> List[float]:
        """Get Swap usage history"""
        return list(self.swap_history)
    
    def get_average_ram_usage(self) -> float:
        """Get average RAM usage"""
        if len(self.ram_history) == 0:
            return 0
        return sum(self.ram_history) / len(self.ram_history)
    
    def is_high_usage(self, threshold: float = Config.MEMORY_THRESHOLD) -> bool:
        """Check if memory usage is above threshold"""
        return self.current_ram.get("percent", 0) > threshold
    
    def get_memory_info_human_readable(self) -> Dict:
        """Get memory info in human-readable format"""
        return {
            "total": bytes_to_human_readable(self.current_ram.get("total", 0)),
            "used": bytes_to_human_readable(self.current_ram.get("used", 0)),
            "available": bytes_to_human_readable(self.current_ram.get("available", 0)),
            "percent": f"{self.current_ram.get('percent', 0):.1f}%"
        }
    
    def get_top_memory_processes(self, n: int = 5) -> List[Dict]:
        """Get top N processes by memory usage"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by memory usage
        processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
        return processes[:n]
    
    def get_stats(self) -> Dict:
        """Get comprehensive memory statistics"""
        return {
            "ram": self.current_ram,
            "swap": self.current_swap,
            "ram_human": self.get_memory_info_human_readable(),
            "average_ram_usage": self.get_average_ram_usage(),
            "top_processes": self.get_top_memory_processes()
        }
    
    def __str__(self):
        hr = self.get_memory_info_human_readable()
        return f"""
Memory Statistics:
  RAM Usage: {hr['percent']}
  Used: {hr['used']} / {hr['total']}
  Available: {hr['available']}
  Swap Usage: {self.current_swap.get('percent', 0):.1f}%
"""