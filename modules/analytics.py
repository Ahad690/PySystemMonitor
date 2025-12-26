"""
Analytics Module
Provides performance analysis and predictions
"""

from collections import deque
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import statistics

class PerformanceAnalytics:
    """Analyze system performance and provide insights"""
    
    def __init__(self, history_size: int = 3600):
        self.history_size = history_size
        
        # Historical data storage
        self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.disk_io_history = deque(maxlen=history_size)
        self.network_history = deque(maxlen=history_size)
        
        # Timestamps
        self.timestamps = deque(maxlen=history_size)
    
    def add_data_point(self, cpu: float, memory: float, 
                       disk_io: float = 0, network: float = 0):
        """Add a new data point"""
        self.cpu_history.append(cpu)
        self.memory_history.append(memory)
        self.disk_io_history.append(disk_io)
        self.network_history.append(network)
        self.timestamps.append(datetime.now())
    
    def get_cpu_stats(self) -> Dict:
        """Get CPU statistics"""
        if not self.cpu_history:
            return {}
        
        data = list(self.cpu_history)
        return {
            "current": data[-1] if data else 0,
            "average": statistics.mean(data),
            "min": min(data),
            "max": max(data),
            "std_dev": statistics.stdev(data) if len(data) > 1 else 0,
            "median": statistics.median(data)
        }
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        if not self.memory_history:
            return {}
        
        data = list(self.memory_history)
        return {
            "current": data[-1] if data else 0,
            "average": statistics.mean(data),
            "min": min(data),
            "max": max(data),
            "std_dev": statistics.stdev(data) if len(data) > 1 else 0,
            "median": statistics.median(data)
        }
    
    def detect_trends(self, data_type: str = "cpu") -> Dict:
        """Detect trends in resource usage"""
        if data_type == "cpu":
            data = list(self.cpu_history)
        elif data_type == "memory":
            data = list(self.memory_history)
        else:
            return {}
        
        if len(data) < 10:
            return {"trend": "insufficient_data"}
        
        # Calculate moving averages
        recent = data[-10:]
        older = data[-30:-10] if len(data) >= 30 else data[:-10]
        
        recent_avg = statistics.mean(recent)
        older_avg = statistics.mean(older) if older else recent_avg
        
        # Determine trend
        diff = recent_avg - older_avg
        
        if abs(diff) < 2:
            trend = "stable"
        elif diff > 0:
            trend = "increasing"
        else:
            trend = "decreasing"
        
        return {
            "trend": trend,
            "recent_average": recent_avg,
            "older_average": older_avg,
            "change": diff,
            "change_percent": (diff / older_avg * 100) if older_avg > 0 else 0
        }
    
    def predict_threshold_breach(self, data_type: str, 
                                 threshold: float) -> Optional[Dict]:
        """Predict when a threshold might be breached"""
        if data_type == "cpu":
            data = list(self.cpu_history)
        elif data_type == "memory":
            data = list(self.memory_history)
        else:
            return None
        
        if len(data) < 30:
            return None
        
        trend = self.detect_trends(data_type)
        if trend["trend"] != "increasing":
            return None
        
        current = data[-1]
        rate = trend["change"] / 20  # change per data point
        
        if rate <= 0:
            return None
        
        points_to_threshold = (threshold - current) / rate
        
        if points_to_threshold <= 0:
            return {"status": "already_breached", "value": current}
        
        return {
            "status": "predicted",
            "current_value": current,
            "threshold": threshold,
            "estimated_time_seconds": points_to_threshold,
            "confidence": "low" if points_to_threshold > 300 else "medium"
        }
    
    def get_peak_hours(self, data_type: str = "cpu") -> List[Dict]:
        """Identify peak usage hours"""
        if data_type == "cpu":
            data = list(self.cpu_history)
        elif data_type == "memory":
            data = list(self.memory_history)
        else:
            return []
        
        timestamps = list(self.timestamps)
        
        if len(data) != len(timestamps):
            return []
        
        # Group by hour
        hourly_data = {}
        for i, ts in enumerate(timestamps):
            hour = ts.hour
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(data[i])
        
        # Calculate average per hour
        hourly_avg = []
        for hour, values in hourly_data.items():
            hourly_avg.append({
                "hour": hour,
                "average": statistics.mean(values),
                "max": max(values),
                "sample_count": len(values)
            })
        
        # Sort by average usage
        hourly_avg.sort(key=lambda x: x["average"], reverse=True)
        
        return hourly_avg[:5]  # Top 5 peak hours
    
    def get_health_score(self) -> Dict:
        """Calculate overall system health score"""
        cpu_stats = self.get_cpu_stats()
        mem_stats = self.get_memory_stats()
        
        if not cpu_stats or not mem_stats:
            return {"score": 100, "status": "unknown"}
        
        # Calculate scores (100 = best, 0 = worst)
        cpu_score = max(0, 100 - cpu_stats.get("average", 0))
        mem_score = max(0, 100 - mem_stats.get("average", 0))
        
        # Penalize high variance
        cpu_variance_penalty = min(20, cpu_stats.get("std_dev", 0))
        mem_variance_penalty = min(20, mem_stats.get("std_dev", 0))
        
        overall_score = (
            (cpu_score - cpu_variance_penalty) * 0.5 +
            (mem_score - mem_variance_penalty) * 0.5
        )
        
        # Determine status
        if overall_score >= 80:
            status = "excellent"
        elif overall_score >= 60:
            status = "good"
        elif overall_score >= 40:
            status = "fair"
        elif overall_score >= 20:
            status = "poor"
        else:
            status = "critical"
        
        return {
            "score": round(overall_score, 1),
            "status": status,
            "cpu_score": round(cpu_score, 1),
            "memory_score": round(mem_score, 1),
            "recommendations": self._generate_recommendations(cpu_stats, mem_stats)
        }
    
    def _generate_recommendations(self, cpu_stats: Dict, 
                                  mem_stats: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if cpu_stats.get("average", 0) > 70:
            recommendations.append("Consider closing CPU-intensive applications")
        
        if mem_stats.get("average", 0) > 80:
            recommendations.append("Consider increasing RAM or closing memory-heavy applications")
        
        if cpu_stats.get("std_dev", 0) > 20:
            recommendations.append("CPU usage is highly variable - check for background processes")
        
        if not recommendations:
            recommendations.append("System is running optimally")
        
        return recommendations
    
    def get_summary_report(self) -> Dict:
        """Generate a comprehensive summary report"""
        return {
            "generated_at": datetime.now().isoformat(),
            "data_points": len(self.cpu_history),
            "cpu_stats": self.get_cpu_stats(),
            "memory_stats": self.get_memory_stats(),
            "cpu_trend": self.detect_trends("cpu"),
            "memory_trend": self.detect_trends("memory"),
            "health_score": self.get_health_score(),
            "peak_cpu_hours": self.get_peak_hours("cpu"),
            "peak_memory_hours": self.get_peak_hours("memory")
        }