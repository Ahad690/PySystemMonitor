"""
Utility Helper Functions
"""

import os
import datetime
from typing import Union

def bytes_to_human_readable(bytes_value: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def seconds_to_human_readable(seconds: int) -> str:
    """Convert seconds to human-readable format"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def get_timestamp() -> str:
    """Get current timestamp"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_directory(path: str) -> None:
    """Ensure directory exists"""
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_percentage(used: Union[int, float], total: Union[int, float]) -> float:
    """Calculate percentage safely"""
    if total == 0:
        return 0.0
    return (used / total) * 100

def truncate_string(s: str, max_length: int = 30) -> str:
    """Truncate string with ellipsis"""
    if len(s) > max_length:
        return s[:max_length-3] + "..."
    return s