"""
Network Monitoring Module
Monitors network I/O, connections, and interface statistics
"""

import psutil
import time
from typing import Dict, List
from collections import deque
from config.settings import Config
from utils.helpers import bytes_to_human_readable

class NetworkMonitor:
    """Monitor network usage and connections"""
    
    def __init__(self, history_length: int = Config.HISTORY_LENGTH):
        self.history_length = history_length
        self.io_history = {
            "bytes_sent": deque(maxlen=history_length),
            "bytes_recv": deque(maxlen=history_length)
        }
        
        self.previous_io = None
        self._last_update = 0
        self.current_rates = {"sent": 0, "recv": 0}
        self.io_counters = {}
    
    def update(self) -> Dict:
        """Update network statistics"""
        current_io = psutil.net_io_counters()
        current_time = time.time()
        
        # Calculate rates
        if self.previous_io and self._last_update:
            time_delta = current_time - self._last_update
            if time_delta > 0:
                self.current_rates = {
                    "sent": (current_io.bytes_sent - self.previous_io.bytes_sent) / time_delta,
                    "recv": (current_io.bytes_recv - self.previous_io.bytes_recv) / time_delta
                }
                self.io_history["bytes_sent"].append(self.current_rates["sent"])
                self.io_history["bytes_recv"].append(self.current_rates["recv"])
        
        self.previous_io = current_io
        self._last_update = current_time
        
        self.io_counters = {
            "bytes_sent": current_io.bytes_sent,
            "bytes_recv": current_io.bytes_recv,
            "packets_sent": current_io.packets_sent,
            "packets_recv": current_io.packets_recv,
            "errin": current_io.errin,
            "errout": current_io.errout,
            "dropin": current_io.dropin,
            "dropout": current_io.dropout
        }
        
        return self.io_counters
    
    def get_current_rates(self) -> Dict:
        """Get current network rates"""
        return {
            "upload": bytes_to_human_readable(self.current_rates["sent"]) + "/s",
            "download": bytes_to_human_readable(self.current_rates["recv"]) + "/s"
        }
    
    def get_total_transfer(self) -> Dict:
        """Get total data transferred"""
        return {
            "sent": bytes_to_human_readable(self.io_counters.get("bytes_sent", 0)),
            "received": bytes_to_human_readable(self.io_counters.get("bytes_recv", 0))
        }
    
    def get_interfaces(self) -> Dict:
        """Get network interface information"""
        interfaces = {}
        
        # Get interface addresses
        for interface, addresses in psutil.net_if_addrs().items():
            interfaces[interface] = {
                "addresses": []
            }
            for addr in addresses:
                interfaces[interface]["addresses"].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
        
        # Get interface stats
        for interface, stats in psutil.net_if_stats().items():
            if interface in interfaces:
                interfaces[interface].update({
                    "isup": stats.isup,
                    "duplex": str(stats.duplex),
                    "speed": stats.speed,
                    "mtu": stats.mtu
                })
        
        return interfaces
    
    def get_connections(self, kind: str = 'inet') -> List[Dict]:
        """Get network connections"""
        connections = []
        try:
            for conn in psutil.net_connections(kind=kind):
                connection_info = {
                    "fd": conn.fd,
                    "family": str(conn.family),
                    "type": str(conn.type),
                    "laddr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "",
                    "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
                    "status": conn.status,
                    "pid": conn.pid
                }
                connections.append(connection_info)
        except psutil.AccessDenied:
            pass
        
        return connections
    
    def get_connection_count(self) -> Dict:
        """Get count of connections by status"""
        counts = {}
        try:
            for conn in psutil.net_connections():
                status = conn.status
                counts[status] = counts.get(status, 0) + 1
        except psutil.AccessDenied:
            pass
        return counts
    
    def get_history(self) -> Dict:
        """Get network I/O history"""
        return {
            "upload": list(self.io_history["bytes_sent"]),
            "download": list(self.io_history["bytes_recv"])
        }
    
    def get_stats(self) -> Dict:
        """Get comprehensive network statistics"""
        return {
            "io_counters": self.io_counters,
            "current_rates": self.get_current_rates(),
            "total_transfer": self.get_total_transfer(),
            "connection_count": self.get_connection_count(),
            "active_interfaces": len([i for i, s in psutil.net_if_stats().items() if s.isup])
        }
    
    def __str__(self):
        rates = self.get_current_rates()
        total = self.get_total_transfer()
        return f"""
Network Statistics:
  Upload: {rates['upload']}
  Download: {rates['download']}
  Total Sent: {total['sent']}
  Total Received: {total['received']}
"""