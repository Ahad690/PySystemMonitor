"""
Alert System Module
Handles alerts and notifications for resource thresholds
"""

import threading
import time
from datetime import datetime
from typing import List, Dict, Callable, Optional
from collections import deque
from config.settings import Config

class Alert:
    """Represents a single alert"""
    
    def __init__(self, alert_type: str, message: str, severity: str = "warning",
                 value: float = 0, threshold: float = 0):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.timestamp = datetime.now()
        self.alert_type = alert_type
        self.message = message
        self.severity = severity  # info, warning, critical
        self.value = value
        self.threshold = threshold
        self.acknowledged = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.alert_type,
            "message": self.message,
            "severity": self.severity,
            "value": self.value,
            "threshold": self.threshold,
            "acknowledged": self.acknowledged
        }
    
    def __str__(self):
        return f"[{self.severity.upper()}] {self.timestamp.strftime('%H:%M:%S')} - {self.message}"


class AlertSystem:
    """Manage system alerts and notifications"""
    
    def __init__(self, max_alerts: int = 100):
        self.alerts = deque(maxlen=max_alerts)
        self.active_alerts = {}
        self.alert_callbacks = []
        self.thresholds = {
            "cpu": Config.CPU_THRESHOLD,
            "memory": Config.MEMORY_THRESHOLD,
            "disk": Config.DISK_THRESHOLD
        }
        self.cooldown = {}  # Prevent alert spam
        self.cooldown_period = 60  # seconds
        self._lock = threading.Lock()
    
    def add_callback(self, callback: Callable):
        """Add a callback function to be called when an alert is triggered"""
        self.alert_callbacks.append(callback)
    
    def remove_callback(self, callback: Callable):
        """Remove a callback function"""
        if callback in self.alert_callbacks:
            self.alert_callbacks.remove(callback)
    
    def _trigger_callbacks(self, alert: Alert):
        """Trigger all registered callbacks"""
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Alert callback error: {e}")
    
    def _is_in_cooldown(self, alert_type: str) -> bool:
        """Check if alert type is in cooldown period"""
        if alert_type in self.cooldown:
            elapsed = time.time() - self.cooldown[alert_type]
            if elapsed < self.cooldown_period:
                return True
        return False
    
    def _set_cooldown(self, alert_type: str):
        """Set cooldown for alert type"""
        self.cooldown[alert_type] = time.time()
    
    def check_cpu(self, value: float) -> Optional[Alert]:
        """Check CPU usage and create alert if needed"""
        if value > self.thresholds["cpu"]:
            if not self._is_in_cooldown("cpu"):
                severity = "critical" if value > 95 else "warning"
                alert = Alert(
                    alert_type="cpu",
                    message=f"High CPU usage detected: {value:.1f}%",
                    severity=severity,
                    value=value,
                    threshold=self.thresholds["cpu"]
                )
                self._add_alert(alert)
                self._set_cooldown("cpu")
                return alert
        return None
    
    def check_memory(self, value: float) -> Optional[Alert]:
        """Check memory usage and create alert if needed"""
        if value > self.thresholds["memory"]:
            if not self._is_in_cooldown("memory"):
                severity = "critical" if value > 95 else "warning"
                alert = Alert(
                    alert_type="memory",
                    message=f"High memory usage detected: {value:.1f}%",
                    severity=severity,
                    value=value,
                    threshold=self.thresholds["memory"]
                )
                self._add_alert(alert)
                self._set_cooldown("memory")
                return alert
        return None
    
    def check_disk(self, value: float, partition: str = "/") -> Optional[Alert]:
        """Check disk usage and create alert if needed"""
        alert_key = f"disk_{partition}"
        if value > self.thresholds["disk"]:
            if not self._is_in_cooldown(alert_key):
                severity = "critical" if value > 95 else "warning"
                alert = Alert(
                    alert_type="disk",
                    message=f"High disk usage on {partition}: {value:.1f}%",
                    severity=severity,
                    value=value,
                    threshold=self.thresholds["disk"]
                )
                self._add_alert(alert)
                self._set_cooldown(alert_key)
                return alert
        return None
    
    def create_custom_alert(self, alert_type: str, message: str, 
                           severity: str = "info") -> Alert:
        """Create a custom alert"""
        alert = Alert(
            alert_type=alert_type,
            message=message,
            severity=severity
        )
        self._add_alert(alert)
        return alert
    
    def _add_alert(self, alert: Alert):
        """Add an alert to the system"""
        with self._lock:
            self.alerts.append(alert)
            self.active_alerts[alert.id] = alert
            self._trigger_callbacks(alert)
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged = True
            return True
        return False
    
    def get_alerts(self, limit: int = 50, 
                  severity: Optional[str] = None,
                  alert_type: Optional[str] = None) -> List[Dict]:
        """Get alerts with optional filtering"""
        alerts = list(self.alerts)
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        if alert_type:
            alerts = [a for a in alerts if a.alert_type == alert_type]
        
        # Return most recent first
        alerts = sorted(alerts, key=lambda x: x.timestamp, reverse=True)
        
        return [a.to_dict() for a in alerts[:limit]]
    
    def get_active_alerts(self) -> List[Dict]:
        """Get unacknowledged alerts"""
        return [a.to_dict() for a in self.active_alerts.values() 
                if not a.acknowledged]
    
    def get_alert_count(self) -> Dict:
        """Get count of alerts by severity"""
        counts = {"info": 0, "warning": 0, "critical": 0}
        for alert in self.alerts:
            counts[alert.severity] = counts.get(alert.severity, 0) + 1
        return counts
    
    def clear_alerts(self):
        """Clear all alerts"""
        with self._lock:
            self.alerts.clear()
            self.active_alerts.clear()
    
    def set_threshold(self, alert_type: str, value: float):
        """Set threshold for an alert type"""
        if alert_type in self.thresholds:
            self.thresholds[alert_type] = value
    
    def get_thresholds(self) -> Dict:
        """Get all thresholds"""
        return self.thresholds.copy()