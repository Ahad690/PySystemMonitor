"""
Command Line Interface
Provides terminal-based interaction with the system monitor
"""

import os
import sys
import time
import threading
from typing import Optional
from datetime import datetime

class CLIInterface:
    """Command-line interface for PySystemMonitor"""
    
    def __init__(self, monitor):
        self.monitor = monitor
        self.running = False
        self.refresh_rate = 1
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("=" * 70)
        print("                    PySystemMonitor v1.0")
        print("           Custom System Monitor & Process Manager")
        print("=" * 70)
        print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
    
    def print_cpu_bar(self, percent: float, width: int = 40):
        """Print CPU usage bar"""
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        color = "\033[92m" if percent < 50 else "\033[93m" if percent < 80 else "\033[91m"
        reset = "\033[0m"
        print(f"  CPU:    [{color}{bar}{reset}] {percent:5.1f}%")
    
    def print_memory_bar(self, percent: float, width: int = 40):
        """Print memory usage bar"""
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        color = "\033[92m" if percent < 50 else "\033[93m" if percent < 80 else "\033[91m"
        reset = "\033[0m"
        print(f"  Memory: [{color}{bar}{reset}] {percent:5.1f}%")
    
    def print_system_overview(self):
        """Print system overview"""
        print("\n┌─ SYSTEM OVERVIEW ─────────────────────────────────────────────────┐")
        
        # CPU
        cpu_stats = self.monitor.cpu_monitor.get_stats()
        self.print_cpu_bar(cpu_stats['current_usage'])
        
        # Memory
        mem_stats = self.monitor.memory_monitor.get_ram_usage()
        self.print_memory_bar(mem_stats.get('percent', 0))
        
        # Network
        net_rates = self.monitor.network_monitor.get_current_rates()
        print(f"  Network: ↑ {net_rates['upload']:<12} ↓ {net_rates['download']}")
        
        # Disk I/O
        disk_rates = self.monitor.disk_monitor.get_io_rates()
        print(f"  Disk:    R {disk_rates['read_rate']:<12} W {disk_rates['write_rate']}")
        
        print("└───────────────────────────────────────────────────────────────────┘")
    
    def print_top_processes(self, n: int = 10):
        """Print top processes"""
        print(f"\n┌─ TOP {n} PROCESSES BY CPU ─────────────────────────────────────────┐")
        print("│  PID      NAME                          CPU%    MEM%    STATUS  │")
        print("├───────────────────────────────────────────────────────────────────┤")
        
        processes = self.monitor.process_manager.get_top_cpu_processes(n)
        for proc in processes:
            pid = str(proc.get('pid', ''))[:8]
            name = proc.get('name', '')[:30]
            cpu = proc.get('cpu_percent', 0) or 0
            mem = proc.get('memory_percent', 0) or 0
            status = proc.get('status', '')[:8]
            print(f"│  {pid:<8} {name:<30} {cpu:6.1f}  {mem:6.1f}  {status:<8}│")
        
        print("└───────────────────────────────────────────────────────────────────┘")
    
    def print_alerts(self, n: int = 5):
        """Print recent alerts"""
        alerts = self.monitor.alert_system.get_alerts(limit=n)
        
        if not alerts:
            return
        
        print(f"\n┌─ RECENT ALERTS ───────────────────────────────────────────────────┐")
        for alert in alerts:
            severity = alert['severity'].upper()
            color = "\033[91m" if severity == "CRITICAL" else "\033[93m" if severity == "WARNING" else "\033[94m"
            reset = "\033[0m"
            msg = alert['message'][:50]
            print(f"│  {color}[{severity:^8}]{reset} {msg:<50}│")
        print("└───────────────────────────────────────────────────────────────────┘")
    
    def print_disk_info(self):
        """Print disk information"""
        print("\n┌─ DISK USAGE ──────────────────────────────────────────────────────┐")
        partitions = self.monitor.disk_monitor.get_partition_summary()
        for p in partitions[:4]:  # Show max 4 partitions
            device = p['device'][:20]
            percent = float(p['percent'].strip('%'))
            filled = int(20 * percent / 100)
            bar = "█" * filled + "░" * (20 - filled)
            color = "\033[92m" if percent < 70 else "\033[93m" if percent < 90 else "\033[91m"
            reset = "\033[0m"
            print(f"│  {device:<20} [{color}{bar}{reset}] {p['percent']:>6}  {p['used']}/{p['total']}│")
        print("└───────────────────────────────────────────────────────────────────┘")
    
    def print_menu(self):
        """Print command menu"""
        print("\n┌─ COMMANDS ─────────────────────────────────────────────────────────┐")
        print("│  [Q] Quit  [R] Refresh  [P] Process List  [K] Kill Process        │")
        print("│  [D] Disk  [N] Network  [A] Alerts       [E] Export Data          │")
        print("│  [H] Health Score       [S] System Info   [C] Clear Alerts        │")
        print("└───────────────────────────────────────────────────────────────────┘")
    
    def display_dashboard(self):
        """Display the main dashboard"""
        self.clear_screen()
        self.print_header()
        self.print_system_overview()
        self.print_top_processes(8)
        self.print_alerts(3)
        self.print_menu()
    
    def run_interactive(self):
        """Run interactive mode"""
        self.running = True
        
        # Start update thread
        def update_loop():
            while self.running:
                self.monitor.update_all()
                time.sleep(self.refresh_rate)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        
        print("Starting PySystemMonitor CLI...")
        time.sleep(1)
        
        while self.running:
            self.display_dashboard()
            
            # Wait for input with timeout
            print("\nEnter command (auto-refresh in 2s): ", end='', flush=True)
            
            import select
            if os.name != 'nt':  # Unix-like systems
                readable, _, _ = select.select([sys.stdin], [], [], 2)
                if readable:
                    cmd = sys.stdin.readline().strip().upper()
                    self.handle_command(cmd)
            else:  # Windows
                time.sleep(2)
    
    def handle_command(self, cmd: str):
        """Handle user command"""
        if cmd == 'Q':
            self.running = False
            print("\nExiting...")
        elif cmd == 'R':
            self.monitor.update_all()
        elif cmd == 'P':
            self.show_all_processes()
        elif cmd == 'K':
            self.kill_process_interactive()
        elif cmd == 'D':
            self.show_disk_details()
        elif cmd == 'N':
            self.show_network_details()
        elif cmd == 'A':
            self.show_all_alerts()
        elif cmd == 'E':
            self.export_data()
        elif cmd == 'H':
            self.show_health_score()
        elif cmd == 'S':
            self.show_system_info()
        elif cmd == 'C':
            self.monitor.alert_system.clear_alerts()
            print("Alerts cleared!")
    
    def show_all_processes(self):
        """Show all processes"""
        self.clear_screen()
        print("\n=== ALL PROCESSES ===\n")
        processes = self.monitor.process_manager.get_process_list()
        print(f"{'PID':<8} {'NAME':<30} {'CPU%':<8} {'MEM%':<8} {'STATUS':<10}")
        print("-" * 70)
        for proc in processes[:30]:
            print(f"{proc.get('pid', ''):<8} {proc.get('name', '')[:28]:<30} "
                  f"{proc.get('cpu_percent', 0) or 0:<8.1f} "
                  f"{proc.get('memory_percent', 0) or 0:<8.1f} {proc.get('status', ''):<10}")
        input("\nPress Enter to continue...")
    
    def kill_process_interactive(self):
        """Interactive process kill"""
        try:
            pid = int(input("Enter PID to kill: "))
            confirm = input(f"Kill process {pid}? (y/n): ")
            if confirm.lower() == 'y':
                result = self.monitor.process_manager.kill_process(pid)
                print(result['message'])
        except ValueError:
            print("Invalid PID")
        input("\nPress Enter to continue...")
    
    def show_health_score(self):
        """Show system health score"""
        self.clear_screen()
        health = self.monitor.analytics.get_health_score()
        print("\n=== SYSTEM HEALTH ===\n")
        print(f"  Overall Score: {health['score']}/100")
        print(f"  Status: {health['status'].upper()}")
        print(f"  CPU Score: {health['cpu_score']}/100")
        print(f"  Memory Score: {health['memory_score']}/100")
        print("\n  Recommendations:")
        for rec in health.get('recommendations', []):
            print(f"    • {rec}")
        input("\nPress Enter to continue...")
    
    def show_system_info(self):
        """Show system information"""
        self.clear_screen()
        print(self.monitor.system_info)
        input("\nPress Enter to continue...")
    
    def show_disk_details(self):
        """Show detailed disk information"""
        self.clear_screen()
        print("\n=== DISK DETAILS ===\n")
        print(self.monitor.disk_monitor)
        input("\nPress Enter to continue...")
    
    def show_network_details(self):
        """Show detailed network information"""
        self.clear_screen()
        print("\n=== NETWORK DETAILS ===\n")
        print(self.monitor.network_monitor)
        
        print("\nConnection Count by Status:")
        for status, count in self.monitor.network_monitor.get_connection_count().items():
            print(f"  {status}: {count}")
        
        input("\nPress Enter to continue...")
    
    def show_all_alerts(self):
        """Show all alerts"""
        self.clear_screen()
        print("\n=== ALL ALERTS ===\n")
        alerts = self.monitor.alert_system.get_alerts(limit=20)
        if not alerts:
            print("No alerts recorded.")
        else:
            for alert in alerts:
                print(f"  [{alert['severity'].upper():^8}] {alert['timestamp']} - {alert['message']}")
        input("\nPress Enter to continue...")
    
    def export_data(self):
        """Export performance data"""
        print("\nExporting data...")
        csv_path = self.monitor.logger.export_to_csv()
        json_path = self.monitor.logger.export_to_json()
        print(f"Exported to:\n  CSV: {csv_path}\n  JSON: {json_path}")
        input("\nPress Enter to continue...")