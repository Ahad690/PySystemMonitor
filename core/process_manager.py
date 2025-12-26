"""
Process Management Module
Lists, monitors, and manages system processes
"""

import psutil
import os
import signal
from typing import Dict, List, Optional
from utils.helpers import bytes_to_human_readable, seconds_to_human_readable

class ProcessManager:
    """Manage and monitor system processes"""
    
    def __init__(self):
        self.processes = []
        self.process_cache = {}
    
    def update(self) -> List[Dict]:
        """Update process list"""
        self.processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 
                                          'memory_percent', 'memory_info', 'status',
                                          'create_time', 'num_threads', 'nice']):
            try:
                pinfo = proc.info
                pinfo['memory_rss'] = pinfo.get('memory_info').rss if pinfo.get('memory_info') else 0
                pinfo['memory_vms'] = pinfo.get('memory_info').vms if pinfo.get('memory_info') else 0
                self.processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return self.processes
    
    def get_process_list(self, sort_by: str = 'cpu_percent', 
                         reverse: bool = True) -> List[Dict]:
        """Get sorted process list"""
        sorted_processes = sorted(
            self.processes,
            key=lambda x: x.get(sort_by, 0) or 0,
            reverse=reverse
        )
        return sorted_processes
    
    def get_process_by_pid(self, pid: int) -> Optional[Dict]:
        """Get detailed information about a specific process"""
        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                return {
                    "pid": proc.pid,
                    "name": proc.name(),
                    "exe": proc.exe(),
                    "cwd": proc.cwd(),
                    "cmdline": proc.cmdline(),
                    "username": proc.username(),
                    "status": proc.status(),
                    "create_time": proc.create_time(),
                    "cpu_percent": proc.cpu_percent(),
                    "memory_percent": proc.memory_percent(),
                    "memory_info": {
                        "rss": proc.memory_info().rss,
                        "vms": proc.memory_info().vms
                    },
                    "num_threads": proc.num_threads(),
                    "num_fds": proc.num_fds() if hasattr(proc, 'num_fds') else 0,
                    "nice": proc.nice(),
                    "io_counters": proc.io_counters()._asdict() if proc.io_counters() else {},
                    "connections": len(proc.connections()),
                    "open_files": len(proc.open_files())
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    
    def get_process_count(self) -> int:
        """Get total number of processes"""
        return len(self.processes)
    
    def get_process_by_status(self) -> Dict:
        """Get process count by status"""
        status_count = {}
        for proc in self.processes:
            status = proc.get('status', 'unknown')
            status_count[status] = status_count.get(status, 0) + 1
        return status_count
    
    def kill_process(self, pid: int, force: bool = False) -> Dict:
        """Kill a process by PID"""
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name()
            
            if force:
                proc.kill()  # SIGKILL
                return {"success": True, "message": f"Process {proc_name} (PID: {pid}) killed forcefully"}
            else:
                proc.terminate()  # SIGTERM
                return {"success": True, "message": f"Process {proc_name} (PID: {pid}) terminated"}
        
        except psutil.NoSuchProcess:
            return {"success": False, "message": f"Process with PID {pid} not found"}
        except psutil.AccessDenied:
            return {"success": False, "message": f"Access denied to terminate PID {pid}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def suspend_process(self, pid: int) -> Dict:
        """Suspend a process"""
        try:
            proc = psutil.Process(pid)
            proc.suspend()
            return {"success": True, "message": f"Process {pid} suspended"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def resume_process(self, pid: int) -> Dict:
        """Resume a suspended process"""
        try:
            proc = psutil.Process(pid)
            proc.resume()
            return {"success": True, "message": f"Process {pid} resumed"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def set_priority(self, pid: int, priority: int) -> Dict:
        """Set process priority (nice value)"""
        try:
            proc = psutil.Process(pid)
            proc.nice(priority)
            return {"success": True, "message": f"Process {pid} priority set to {priority}"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_top_cpu_processes(self, n: int = 10) -> List[Dict]:
        """Get top N processes by CPU usage"""
        return self.get_process_list(sort_by='cpu_percent')[:n]
    
    def get_top_memory_processes(self, n: int = 10) -> List[Dict]:
        """Get top N processes by memory usage"""
        return self.get_process_list(sort_by='memory_percent')[:n]
    
    def search_process(self, name: str) -> List[Dict]:
        """Search processes by name"""
        matches = []
        for proc in self.processes:
            if name.lower() in proc.get('name', '').lower():
                matches.append(proc)
        return matches
    
    def get_process_tree(self, pid: int) -> Dict:
        """Get process tree (parent and children)"""
        try:
            proc = psutil.Process(pid)
            parent = proc.parent()
            children = proc.children(recursive=True)
            
            return {
                "process": {"pid": pid, "name": proc.name()},
                "parent": {"pid": parent.pid, "name": parent.name()} if parent else None,
                "children": [{"pid": c.pid, "name": c.name()} for c in children]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_summary(self) -> Dict:
        """Get process summary"""
        total_cpu = sum(p.get('cpu_percent', 0) or 0 for p in self.processes)
        total_memory = sum(p.get('memory_percent', 0) or 0 for p in self.processes)
        
        return {
            "total_processes": len(self.processes),
            "status_breakdown": self.get_process_by_status(),
            "total_cpu_usage": total_cpu,
            "total_memory_usage": total_memory,
            "top_cpu": self.get_top_cpu_processes(5),
            "top_memory": self.get_top_memory_processes(5)
        }