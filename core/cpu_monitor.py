"""
CPU Monitoring Module
Monitors CPU usage, frequency, and per-core statistics
"""

import psutil
import time
from collections import deque
from typing import List, Dict
from config.settings import Config

class CPUMonitor:
    """Monitor CPU usage and statistics"""
    
    def __init__(self, history_length: int = Config.HISTORY_LENGTH):
        self.history_length = history_length
        self.usage_history = deque(maxlen=history_length)
        self.per_core_history = {}
        
        # Initialize per-core history
        for i in range(psutil.cpu_count()):
            self.per_core_history[i] = deque(maxlen=history_length)
        
        self._last_update = 0
        self.current_usage = 0
        self.per_core_usage = []
    
    def update(self) -> float:
        """Update CPU statistics"""
        # Overall CPU usage
        self.current_usage = psutil.cpu_percent(interval=0.1)
        self.usage_history.append(self.current_usage)
        
        # Per-core usage
        self.per_core_usage = psutil.cpu_percent(interval=0.1, percpu=True)
        for i, usage in enumerate(self.per_core_usage):
            if i in self.per_core_history:
                self.per_core_history[i].append(usage)
        
        self._last_update = time.time()
        return self.current_usage
    
    def get_current_usage(self) -> float:
        """Get current CPU usage percentage"""
        return self.current_usage
    
    def get_per_core_usage(self) -> List[float]:
        """Get CPU usage per core"""
        return self.per_core_usage
    
    def get_frequency(self) -> Dict:
        """Get CPU frequency information"""
        freq = psutil.cpu_freq()
        if freq:
            return {
                "current": freq.current,
                "min": freq.min,
                "max": freq.max
            }
        return {"current": 0, "min": 0, "max": 0}
    
    def get_load_average(self) -> tuple:
        """Get system load average (Unix-like systems)"""
        try:
            return psutil.getloadavg()
        except AttributeError:
            # Windows doesn't support getloadavg
            return (0, 0, 0)
    
    def get_history(self) -> List[float]:
        """Get CPU usage history"""
        return list(self.usage_history)
    
    def get_average_usage(self) -> float:
        """Get average CPU usage from history"""
        if len(self.usage_history) == 0:
            return 0
        return sum(self.usage_history) / len(self.usage_history)
    
    def get_peak_usage(self) -> float:
        """Get peak CPU usage from history"""
        if len(self.usage_history) == 0:
            return 0
        return max(self.usage_history)
    
    def is_high_usage(self, threshold: float = Config.CPU_THRESHOLD) -> bool:
        """Check if CPU usage is above threshold"""
        return self.current_usage > threshold
    
    def get_stats(self) -> Dict:
        """Get comprehensive CPU statistics"""
        freq = self.get_frequency()
        return {
            "current_usage": self.current_usage,
            "average_usage": self.get_average_usage(),
            "peak_usage": self.get_peak_usage(),
            "per_core_usage": self.per_core_usage,
            "frequency_current": freq["current"],
            "frequency_max": freq["max"],
            "core_count": psutil.cpu_count(),
            "physical_cores": psutil.cpu_count(logical=False),
            "load_average": self.get_load_average()
        }
    
    def __str__(self):
        stats = self.get_stats()
        return f"""
CPU Statistics:
  Current Usage: {stats['current_usage']:.1f}%
  Average Usage: {stats['average_usage']:.1f}%
  Peak Usage: {stats['peak_usage']:.1f}%
  Cores: {stats['physical_cores']} physical, {stats['core_count']} logical
  Frequency: {stats['frequency_current']:.0f} MHz
"""