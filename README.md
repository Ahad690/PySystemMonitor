# PySystemMonitor 🖥️

**PySystemMonitor** is a comprehensive, cross-platform system monitoring and process management tool written in Python. It is designed to provide real-time insights into system performance, health analytics, and resource usage with both a rich Graphical User Interface (GUI) and a lightweight Command-Line Interface (CLI).

## 🚀 Key Features

*   **Real-Time Monitoring**: Track CPU, Memory (RAM/Swap), Disk I/O, and Network traffic in real-time.
*   **Dual Interfaces**:
    *   **GUI**: A modern, dark-themed dashboard built with Tkinter for visualizing system metrics.
    *   **CLI**: A terminal-based interactive dashboard for headless environments or quick checks.
*   **Process Manager**: View, search, and manage active processes. Supports killing, suspending, and resuming processes.
*   **System Health Score**: An intelligent scoring system (0-100) that analyzes resource trends and stability to provide an overall system health rating and actionable recommendations.
*   **Smart Alerts**: Configurable thresholds for CPU, Memory, and Disk usage with visual notifications and logging.
*   **Historical Analytics**: prediction of resource exhaustion and trend analysis (e.g., "CPU usage is increasing").
*   **Data Export**: Built-in capability to export performance logs to CSV or JSON formats for offline analysis.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ahad690/PySystemMonitor.git
    cd PySystemMonitor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 Usage

You can run PySystemMonitor in different modes depending on your needs.

### Graphical Interface (Default)
Launch the full GUI dashboard:
```bash
python main.py
```
*Navigating the GUI:*
*   **Overview**: Summary of all system resources.
*   **Processes**: Table of running processes. Right-click or use buttons to manage.
*   **Performance**: Real-time graphs for CPU and Memory.
*   **Disk/Network**: Detailed stats for storage and network adapters.
*   **Alerts**: Log of all system alerts.

### Command-Line Interface
Launch the terminal-based dashboard:
```bash
python main.py --cli
```
*CLI Controls:*
*   `R`: Refresh data
*   `P`: Process list
*   `K`: Kill process
*   `H`: Health score
*   `Q`: Quit

### Background Mode
Run without any UI (useful for logging only):
```bash
python main.py --no-ui
```

## 📂 Project Structure

```
PySystemMonitor/
├── core/               # Data collection modules (CPU, Mem, Disk, Net)
├── interfaces/         # GUI and CLI implementation
├── modules/            # Analytics, Logger, Alert System
├── utils/              # Helper functions
├── config/             # Configuration settings
├── logs/               # Log files storage
├── main.py             # Entry point
└── requirements.txt    # Project dependencies
```

## 🛠️ Configuration

You can customize the application behavior in `config/settings.py`:
*   Update intervals
*   Alert thresholds (CPU %, Memory %)
*   Log file settings
*   Window dimensions

## 📄 License
This project is open-source and available for educational and personal use.

---
*Developed as an Operating Systems Lab Project to demonstrate system design and resource management concepts.*
