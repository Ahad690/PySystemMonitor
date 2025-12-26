"""
Logger Module
Handles logging of system events and performance data
"""

import os
import json
import csv
import logging
from datetime import datetime
from typing import Dict, List, Optional
from logging.handlers import RotatingFileHandler
from config.settings import Config
from utils.helpers import ensure_directory

class SystemLogger:
    """Handle system logging and data export"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        ensure_directory(log_dir)
        
        # Setup main logger
        self.logger = logging.getLogger("PySystemMonitor")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler with rotation
        log_file = os.path.join(log_dir, "system_monitor.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=Config.LOG_MAX_SIZE,
            backupCount=Config.LOG_BACKUP_COUNT
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Performance data storage
        self.performance_data = []
        self.max_data_points = 10000
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_alert(self, alert: Dict):
        """Log an alert"""
        severity = alert.get("severity", "info")
        message = f"ALERT [{alert.get('type')}]: {alert.get('message')}"
        
        if severity == "critical":
            self.critical(message)
        elif severity == "warning":
            self.warning(message)
        else:
            self.info(message)
    
    def log_performance(self, data: Dict):
        """Log performance data point"""
        data["timestamp"] = datetime.now().isoformat()
        self.performance_data.append(data)
        
        # Trim if exceeds max
        if len(self.performance_data) > self.max_data_points:
            self.performance_data = self.performance_data[-self.max_data_points:]
    
    def export_to_csv(self, filename: Optional[str] = None) -> str:
        """Export performance data to CSV"""
        if not filename:
            filename = f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.log_dir, filename)
        
        if not self.performance_data:
            return ""
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.performance_data[0].keys())
            writer.writeheader()
            writer.writerows(self.performance_data)
        
        self.info(f"Performance data exported to {filepath}")
        return filepath
    
    def export_to_json(self, filename: Optional[str] = None) -> str:
        """Export performance data to JSON"""
        if not filename:
            filename = f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.log_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.performance_data, f, indent=2)
        
        self.info(f"Performance data exported to {filepath}")
        return filepath
    
    def get_performance_data(self, limit: int = 100) -> List[Dict]:
        """Get recent performance data"""
        return self.performance_data[-limit:]
    
    def clear_performance_data(self):
        """Clear stored performance data"""
        self.performance_data = []
    
    def get_log_files(self) -> List[str]:
        """Get list of log files"""
        files = []
        for f in os.listdir(self.log_dir):
            if f.endswith('.log') or f.endswith('.csv') or f.endswith('.json'):
                files.append(os.path.join(self.log_dir, f))
        return files