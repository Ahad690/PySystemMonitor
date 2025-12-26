# System Design, Enhancement, and Comparative Analysis Report
## Operating Systems Lab Project

**Project Name:** PySystemMonitor
**Repository:** [https://github.com/Ahad690/PySystemMonitor](https://github.com/Ahad690/PySystemMonitor)

---

### 1. Project Overview

The objective of this project was to design and implement a custom system monitoring tool, **PySystemMonitor**, by studying existing real-world systems like **Windows Task Manager** and **htop**. The project involved analyzing the core functionalities of these reference systems—such as process management, resource tracking, and performance visualization—and embedding them into a custom, modular architecture. 

The developed system demonstrates core operating system concepts including process scheduling inspection, memory management visualization, and I/O monitoring, while introducing novel features like AI-driven health scoring and historic analytics.

---

### 2. Problem Statement

The goal was to:
* Build a **custom system monitor** inspired by standard OS utilities.
* Implement **primary functionalities**: Real-time CPU/Memory tracking, Process listing/killing, and Disk/Network I/O monitoring.
* Introduce **novel enhancements**: System Health Score, Historical Analytics, and cross-platform compatibility via Python.
* Evaluate the system through a **comparative analysis** against the standard Windows Task Manager.

---

### 3. Reference System (Baseline)

For comparison, **Windows Task Manager** was selected as the baseline system.

**Key Analysis of Reference System:**
* **Strengths:** Deep OS integration, low overhead, immediate control over processes.
* **Limitations:** Limited historical data (real-time only), lack of high-level "health" interpretation for non-technical users, and interface clutter.

---

### 4. Proposed System (PySystemMonitor)

**PySystemMonitor** is a custom-designed, cross-platform monitoring solution built with Python. It replicates the essential features of the reference system while embedding them in a user-friendly, dual-interface (GUI & CLI) architecture.

**Core Architecture:**
1.  **Aggregator Core:** A central `SystemMonitor` class that orchestrates specialized collectors (`CPUMonitor`, `MemoryMonitor`, `ProcessManager`).
2.  **Modular Design:** Decoupled data collection (Backend) from presentation (Frontend), allowing for both GUI (Tkinter) and CLI (Terminal) interfaces.
3.  **Analytics Engine:** A dedicated module for statistical analysis and trend prediction.

---

### 5. Novelty and Enhancements

PySystemMonitor introduces several enhancements over the standard Task Manager:

1.  **System Health Score:** Instead of just showing raw numbers, the system calculates a composite score (0-100) indicating overall system health, making it easier for casual users to understand system status.
2.  **Intelligent Recommendations:** The system analyzes resource usage trends to provide actionable advice (e.g., "High memory variance detected," "Consider closing background apps").
3.  **Dual Interface:** Unlike Task Manager (GUI only) or htop (CLI only), PySystemMonitor offers **both** a rich GUI and a lightweight CLI in a single package.
4.  **Log Export:** Built-in capability to export performance data to JSON and CSV for offline analysis.

---

### 6. Comparative Analysis

The following table compares the Reference System (Windows Task Manager) with the Proposed System (PySystemMonitor):

| Feature | Reference System (Task Manager) | Proposed System (PySystemMonitor) |
| :--- | :--- | :--- |
| **Real-time Monitoring** | Excellent (Kernel level hook) | Good (via psutil wrapper) |
| **Process Management** | Full Control (Kill, Priority, Affinity) | Essential Control (Kill, Suspend, Resume) |
| **User Interface** | GUI Only | **GUI + CLI (Terminal)** |
| **Health Interpretation** | Raw Numbers Only | **Health Score & Recommendations** |
| **Historical Data** | Short-term graphs | **Session-based Analytics & Logs** |
| **Data Export** | distinct tools required (perfmon) | **Built-in CSV/JSON Export** |
| **Platform** | Windows Only | **Cross-Platform (Windows/Linux/macOS)** |

---

### 7. Learning Outcomes

Through this project, the following learning outcomes were achieved:
* **OS Internals:** Gained deep understanding of how OS exposes process and resource information (e.g., `/proc` filesystem concepts, Windows API).
* **Concurrency:** Implemented threaded data collection to ensure the UI remains responsive while polling system resources.
* **System Design:** Designed a modular architecture separating data acquisition, processing, and visualization.
* **Resource Management:** Learned practical challenges in monitoring resources efficiently without becoming a resource hog itself.

---

### 8. Conclusion

PySystemMonitor successfully fulfills the OS Lab requirements by replicating the core functionality of established system monitors while introducing meaningful novelties like the Health Score algorithm and dual-interface design. The project demonstrates a practical application of operating system principles, resulting in a functional tool that offers unique advantages in usability and flexibility compared to the reference system.
