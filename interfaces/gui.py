"""
Graphical User Interface
Provides a GUI for the system monitor using tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from datetime import datetime
from config.settings import Config

class GUIInterface:
    """Graphical interface for PySystemMonitor"""
    
    def __init__(self, monitor):
        self.monitor = monitor
        self.root = None
        self.running = False
        
        # Data for graphs
        self.cpu_data = []
        self.memory_data = []
        self.max_data_points = 60
    
    def create_window(self):
        """Create the main window"""
        self.root = tk.Tk()
        self.root.title("PySystemMonitor - System Monitor & Process Manager")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg='#1e1e1e')
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_overview_tab()
        self.create_processes_tab()
        self.create_performance_tab()
        self.create_disk_tab()
        self.create_network_tab()
        self.create_alerts_tab()
        
        # Status bar
        self.create_status_bar()
        
        # Apply dark theme
        self.apply_theme()
    
    def apply_theme(self):
        """Apply dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#2d2d2d'
        fg_color = '#ffffff'
        selected_bg = '#404040'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background='#404040', foreground=fg_color)
        style.configure('TNotebook', background=bg_color)
        style.configure('TNotebook.Tab', background='#404040', foreground=fg_color, padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#505050')])
        
        # Treeview
        style.configure('Treeview', 
                       background=bg_color, 
                       foreground=fg_color, 
                       fieldbackground=bg_color)
        style.map('Treeview', background=[('selected', selected_bg)])
        style.configure('Treeview.Heading', 
                       background='#404040', 
                       foreground=fg_color)
    
    def create_overview_tab(self):
        """Create the overview tab"""
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text='Overview')
        
        # CPU Frame
        cpu_frame = ttk.LabelFrame(self.overview_frame, text="CPU Usage")
        cpu_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.cpu_label = ttk.Label(cpu_frame, text="CPU: 0%", font=('Helvetica', 14))
        self.cpu_label.pack(pady=5)
        
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=400, mode='determinate')
        self.cpu_progress.pack(pady=5, padx=10, fill=tk.X)
        
        # Memory Frame
        mem_frame = ttk.LabelFrame(self.overview_frame, text="Memory Usage")
        mem_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.mem_label = ttk.Label(mem_frame, text="Memory: 0%", font=('Helvetica', 14))
        self.mem_label.pack(pady=5)
        
        self.mem_progress = ttk.Progressbar(mem_frame, length=400, mode='determinate')
        self.mem_progress.pack(pady=5, padx=10, fill=tk.X)
        
        # System Info Frame
        info_frame = ttk.LabelFrame(self.overview_frame, text="System Information")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.system_info_text = tk.Text(info_frame, height=10, bg='#2d2d2d', fg='#ffffff')
        self.system_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Populate system info
        info = self.monitor.system_info.get_summary()
        info_str = f"""
        Operating System: {info['os']}
        Hostname: {info['hostname']}
        Architecture: {info['architecture']}
        CPU Cores: {info['cpu_cores']}
        IP Address: {info['ip_address']}
        Uptime: {info['uptime']}
        """
        self.system_info_text.insert(tk.END, info_str)
        self.system_info_text.config(state=tk.DISABLED)
    
    def create_processes_tab(self):
        """Create the processes tab"""
        self.processes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.processes_frame, text='Processes')
        
        # Toolbar
        toolbar = ttk.Frame(self.processes_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Refresh", command=self.refresh_processes).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Kill Process", command=self.kill_selected_process).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Suspend", command=self.suspend_selected_process).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Resume", command=self.resume_selected_process).pack(side=tk.LEFT, padx=2)
        
        # Search
        ttk.Label(toolbar, text="Search:").pack(side=tk.LEFT, padx=(20, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        self.search_var.trace('w', self.filter_processes)
        
        # Process tree
        columns = ('pid', 'name', 'cpu', 'memory', 'status', 'threads')
        self.process_tree = ttk.Treeview(self.processes_frame, columns=columns, show='headings')
        
        self.process_tree.heading('pid', text='PID')
        self.process_tree.heading('name', text='Name')
        self.process_tree.heading('cpu', text='CPU %')
        self.process_tree.heading('memory', text='Memory %')
        self.process_tree.heading('status', text='Status')
        self.process_tree.heading('threads', text='Threads')
        
        self.process_tree.column('pid', width=80)
        self.process_tree.column('name', width=200)
        self.process_tree.column('cpu', width=80)
        self.process_tree.column('memory', width=80)
        self.process_tree.column('status', width=100)
        self.process_tree.column('threads', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.processes_frame, orient=tk.VERTICAL, 
                                  command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_performance_tab(self):
        """Create the performance tab with graphs"""
        self.performance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.performance_frame, text='Performance')
        
        # Canvas for graphs
        self.perf_canvas = tk.Canvas(self.performance_frame, bg='#1e1e1e', 
                                     highlightthickness=0)
        self.perf_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Health score display
        health_frame = ttk.LabelFrame(self.performance_frame, text="System Health")
        health_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.health_label = ttk.Label(health_frame, text="Health Score: --/100", 
                                      font=('Helvetica', 16, 'bold'))
        self.health_label.pack(pady=10)
        
        self.health_status = ttk.Label(health_frame, text="Status: Unknown", 
                                       font=('Helvetica', 12))
        self.health_status.pack(pady=5)
    
    def create_disk_tab(self):
        """Create the disk tab"""
        self.disk_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.disk_frame, text='Disk')
        
        # Disk tree
        columns = ('device', 'mountpoint', 'total', 'used', 'free', 'percent')
        self.disk_tree = ttk.Treeview(self.disk_frame, columns=columns, show='headings')
        
        self.disk_tree.heading('device', text='Device')
        self.disk_tree.heading('mountpoint', text='Mount Point')
        self.disk_tree.heading('total', text='Total')
        self.disk_tree.heading('used', text='Used')
        self.disk_tree.heading('free', text='Free')
        self.disk_tree.heading('percent', text='Usage %')
        
        self.disk_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # I/O rates
        io_frame = ttk.LabelFrame(self.disk_frame, text="Disk I/O")
        io_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.disk_io_label = ttk.Label(io_frame, text="Read: -- | Write: --", 
                                       font=('Helvetica', 12))
        self.disk_io_label.pack(pady=10)
    
    def create_network_tab(self):
        """Create the network tab"""
        self.network_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.network_frame, text='Network')
        
        # Network stats
        stats_frame = ttk.LabelFrame(self.network_frame, text="Network Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.net_upload_label = ttk.Label(stats_frame, text="Upload: 0 B/s", 
                                          font=('Helvetica', 14))
        self.net_upload_label.pack(pady=5)
        
        self.net_download_label = ttk.Label(stats_frame, text="Download: 0 B/s", 
                                            font=('Helvetica', 14))
        self.net_download_label.pack(pady=5)
        
        self.net_total_label = ttk.Label(stats_frame, text="Total: Sent 0 | Received 0", 
                                         font=('Helvetica', 12))
        self.net_total_label.pack(pady=5)
        
        # Connections
        conn_frame = ttk.LabelFrame(self.network_frame, text="Active Connections")
        conn_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.conn_label = ttk.Label(conn_frame, text="Loading...", font=('Helvetica', 12))
        self.conn_label.pack(pady=10)
    
    def create_alerts_tab(self):
        """Create the alerts tab"""
        self.alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alerts_frame, text='Alerts')
        
        # Toolbar
        toolbar = ttk.Frame(self.alerts_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Clear All", command=self.clear_alerts).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Export", command=self.export_alerts).pack(side=tk.LEFT, padx=2)
        
        # Thresholds
        ttk.Label(toolbar, text="CPU Threshold:").pack(side=tk.LEFT, padx=(20, 5))
        self.cpu_threshold_var = tk.StringVar(value=str(Config.CPU_THRESHOLD))
        ttk.Entry(toolbar, textvariable=self.cpu_threshold_var, width=5).pack(side=tk.LEFT)
        
        ttk.Label(toolbar, text="Memory Threshold:").pack(side=tk.LEFT, padx=(10, 5))
        self.mem_threshold_var = tk.StringVar(value=str(Config.MEMORY_THRESHOLD))
        ttk.Entry(toolbar, textvariable=self.mem_threshold_var, width=5).pack(side=tk.LEFT)
        
        ttk.Button(toolbar, text="Apply", command=self.apply_thresholds).pack(side=tk.LEFT, padx=10)
        
        # Alerts list
        columns = ('time', 'type', 'severity', 'message')
        self.alerts_tree = ttk.Treeview(self.alerts_frame, columns=columns, show='headings')
        
        self.alerts_tree.heading('time', text='Time')
        self.alerts_tree.heading('type', text='Type')
        self.alerts_tree.heading('severity', text='Severity')
        self.alerts_tree.heading('message', text='Message')
        
        self.alerts_tree.column('time', width=150)
        self.alerts_tree.column('type', width=100)
        self.alerts_tree.column('severity', width=100)
        self.alerts_tree.column('message', width=400)
        
        self.alerts_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = ttk.Label(self.status_bar, text="")
        self.time_label.pack(side=tk.RIGHT, padx=10)
    
    def update_display(self):
        """Update all display elements"""
        try:
            # Update CPU
            cpu_percent = self.monitor.cpu_monitor.get_current_usage()
            self.cpu_label.config(text=f"CPU: {cpu_percent:.1f}%")
            self.cpu_progress['value'] = cpu_percent
            
            # Update Memory
            mem_percent = self.monitor.memory_monitor.get_ram_percent()
            self.mem_label.config(text=f"Memory: {mem_percent:.1f}%")
            self.mem_progress['value'] = mem_percent
            
            # Update Network
            rates = self.monitor.network_monitor.get_current_rates()
            self.net_upload_label.config(text=f"Upload: {rates['upload']}")
            self.net_download_label.config(text=f"Download: {rates['download']}")
            
            total = self.monitor.network_monitor.get_total_transfer()
            self.net_total_label.config(text=f"Total: Sent {total['sent']} | Received {total['received']}")
            
            # Update Disk I/O
            io_rates = self.monitor.disk_monitor.get_io_rates()
            self.disk_io_label.config(text=f"Read: {io_rates['read_rate']} | Write: {io_rates['write_rate']}")
            
            # Update Health Score
            health = self.monitor.analytics.get_health_score()
            self.health_label.config(text=f"Health Score: {health['score']}/100")
            self.health_status.config(text=f"Status: {health['status'].upper()}")
            
            # Update Connection Count
            conn_count = self.monitor.network_monitor.get_connection_count()
            conn_str = " | ".join([f"{k}: {v}" for k, v in conn_count.items()])
            self.conn_label.config(text=conn_str if conn_str else "No connections")
            
            # Update Status Bar
            self.time_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Store data for graphs
            self.cpu_data.append(cpu_percent)
            self.memory_data.append(mem_percent)
            if len(self.cpu_data) > self.max_data_points:
                self.cpu_data = self.cpu_data[-self.max_data_points:]
                self.memory_data = self.memory_data[-self.max_data_points:]
            
            # Draw graphs
            self.draw_graphs()
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
    
    def draw_graphs(self):
        """Draw performance graphs on canvas"""
        self.perf_canvas.delete("all")
        
        width = self.perf_canvas.winfo_width()
        height = self.perf_canvas.winfo_height() // 2
        
        if width < 100 or height < 50:
            return
        
        # Draw CPU graph
        self.draw_line_graph(self.cpu_data, 0, 0, width, height, 
                            "#00ff00", "CPU Usage")
        
        # Draw Memory graph
        self.draw_line_graph(self.memory_data, 0, height, width, height, 
                            "#00ffff", "Memory Usage")
    
    def draw_line_graph(self, data, x, y, width, height, color, title):
        """Draw a line graph"""
        if not data:
            return
        
        # Background
        self.perf_canvas.create_rectangle(x, y, x + width, y + height, 
                                          fill='#2d2d2d', outline='#404040')
        
        # Title
        self.perf_canvas.create_text(x + 10, y + 15, text=title, 
                                     fill='#ffffff', anchor='w', font=('Helvetica', 10))
        
        # Current value
        current = data[-1] if data else 0
        self.perf_canvas.create_text(x + width - 10, y + 15, 
                                     text=f"{current:.1f}%", 
                                     fill=color, anchor='e', font=('Helvetica', 12, 'bold'))
        
        # Draw line
        if len(data) > 1:
            points = []
            margin = 30
            graph_width = width - 2 * margin
            graph_height = height - 50
            
            for i, val in enumerate(data):
                px = x + margin + (i / (len(data) - 1)) * graph_width
                py = y + height - margin - (val / 100) * graph_height
                points.extend([px, py])
            
            if len(points) >= 4:
                self.perf_canvas.create_line(points, fill=color, width=2, smooth=True)
        
        # Draw grid lines
        for i in range(5):
            line_y = y + 30 + (i * (height - 50) / 4)
            self.perf_canvas.create_line(x + 30, line_y, x + width - 30, line_y, 
                                         fill='#404040', dash=(2, 4))
            val = 100 - (i * 25)
            self.perf_canvas.create_text(x + 25, line_y, text=str(val), 
                                         fill='#888888', anchor='e', font=('Helvetica', 8))
    
    def refresh_processes(self):
        """Refresh process list"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Get processes
        self.monitor.process_manager.update()
        processes = self.monitor.process_manager.get_process_list()
        
        # Filter if search term exists
        search_term = self.search_var.get().lower()
        
        for proc in processes:
            if search_term and search_term not in proc.get('name', '').lower():
                continue
            
            self.process_tree.insert('', tk.END, values=(
                proc.get('pid', ''),
                proc.get('name', ''),
                f"{proc.get('cpu_percent', 0) or 0:.1f}",
                f"{proc.get('memory_percent', 0) or 0:.1f}",
                proc.get('status', ''),
                proc.get('num_threads', '')
            ))
    
    def filter_processes(self, *args):
        """Filter processes based on search"""
        self.refresh_processes()
    
    def refresh_disks(self):
        """Refresh disk information"""
        # Clear existing items
        for item in self.disk_tree.get_children():
            self.disk_tree.delete(item)
        
        # Get disk info
        partitions = self.monitor.disk_monitor.get_partition_summary()
        
        for p in partitions:
            self.disk_tree.insert('', tk.END, values=(
                p['device'],
                p['mountpoint'],
                p['total'],
                p['used'],
                p['free'],
                p['percent']
            ))
    
    def refresh_alerts(self):
        """Refresh alerts list"""
        # Clear existing items
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
        
        # Get alerts
        alerts = self.monitor.alert_system.get_alerts(limit=50)
        
        for alert in alerts:
            tag = alert['severity']
            self.alerts_tree.insert('', tk.END, values=(
                alert['timestamp'],
                alert['type'],
                alert['severity'].upper(),
                alert['message']
            ), tags=(tag,))
        
        # Configure tags for colors
        self.alerts_tree.tag_configure('critical', foreground='#ff4444')
        self.alerts_tree.tag_configure('warning', foreground='#ffaa00')
        self.alerts_tree.tag_configure('info', foreground='#4444ff')
    
    def kill_selected_process(self):
        """Kill the selected process"""
        selected = self.process_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a process first")
            return
        
        item = self.process_tree.item(selected[0])
        pid = int(item['values'][0])
        name = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Kill process {name} (PID: {pid})?"):
            result = self.monitor.process_manager.kill_process(pid)
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.refresh_processes()
            else:
                messagebox.showerror("Error", result['message'])
    
    def suspend_selected_process(self):
        """Suspend the selected process"""
        selected = self.process_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a process first")
            return
        
        item = self.process_tree.item(selected[0])
        pid = int(item['values'][0])
        
        result = self.monitor.process_manager.suspend_process(pid)
        messagebox.showinfo("Result", result['message'])
        self.refresh_processes()
    
    def resume_selected_process(self):
        """Resume the selected process"""
        selected = self.process_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a process first")
            return
        
        item = self.process_tree.item(selected[0])
        pid = int(item['values'][0])
        
        result = self.monitor.process_manager.resume_process(pid)
        messagebox.showinfo("Result", result['message'])
        self.refresh_processes()
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.monitor.alert_system.clear_alerts()
        self.refresh_alerts()
        messagebox.showinfo("Info", "All alerts cleared")
    
    def export_alerts(self):
        """Export alerts to file"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            import json
            alerts = self.monitor.alert_system.get_alerts()
            with open(filepath, 'w') as f:
                json.dump(alerts, f, indent=2)
            messagebox.showinfo("Success", f"Alerts exported to {filepath}")
    
    def apply_thresholds(self):
        """Apply new alert thresholds"""
        try:
            cpu_threshold = float(self.cpu_threshold_var.get())
            mem_threshold = float(self.mem_threshold_var.get())
            
            self.monitor.alert_system.set_threshold('cpu', cpu_threshold)
            self.monitor.alert_system.set_threshold('memory', mem_threshold)
            
            messagebox.showinfo("Success", "Thresholds updated")
        except ValueError:
            messagebox.showerror("Error", "Invalid threshold values")
    
    def update_loop(self):
        """Main update loop"""
        if self.running:
            self.monitor.update_all()
            self.update_display()
            self.refresh_alerts()
            self.refresh_disks()
            # Note: We don't auto-refresh processes every cycle to avoid UI flickering/selection loss
            # But we could add a slower timer for it
            self.root.after(Config.REFRESH_RATE, self.update_loop)
    
    def on_close(self):
        """Handle window close"""
        self.running = False
        if self.root:
            self.root.destroy()
            self.root = None
    
    def run(self):
        """Start the GUI application"""
        self.create_window()
        self.running = True
        
        # Initial population
        self.refresh_disks()
        self.refresh_processes()
        
        # Start update loop
        self.update_loop()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Start main loop
        self.root.mainloop()
        