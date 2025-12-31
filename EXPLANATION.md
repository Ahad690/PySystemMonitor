# Technical Explanation: PySystemMonitor-PS Enterprise Edition

This document details the architecture of the expanded "Enterprise Edition" covering OS Labs 5-11.

## 🖥️ Alternative GUI (`PySystemMonitor-GUI.ps1`)

A standalone Windows Forms interface was added to demonstrate all labs without browser dependencies.

### Interface Breakdown

| Feature / Button | Lab | Description | Why it was added |
| :--- | :--- | :--- | :--- |
| **Critical Services** | **Lab 6** (Diagnostics) | Lists critical services (e.g., DNS, Spooler) with color-coded status (Green=Running, Red=Stopped). | Demonstrates automated system health checks beyond just CPU/RAM. |
| **Kill Button** | **Lab 5** (Automation) | Terminates the selected process in the "Top Processes" list. | Demonstrates safe action execution (`Stop-Process -Force`) triggered by user input. |
| **Start Background Job** | **Lab 7** (Parallelism) | Launches a `Start-Job` that runs for 5 seconds in the background without freezing the UI. | Proves the concept of asynchronous execution/multithreading in PowerShell. |
| **Simulate Parallel** | **Lab 7** (Parallelism) | Runs a loop of tasks using jobs/parallel logic. | Shows how to process multiple items at once to improve performance. |
| **Agentic Insights** | **Lab 8** (Agentic AI) | Analyze Button checks system state (CPU > 80%?) and prints recommendations. | Simulates an "AI" decision engine that converts raw metrics into actionable advice. |
| **Disk Cleanup** | **Lab 9** (Automation) | Simulates clearing temporary files. | Shows how the tool can perform maintenance tasks automatically. |
| **Large Files** | **Lab 11** (Adv Ops) | Scans `C:\Users` for files > 100MB in a background thread. | Demonstrates advanced file system operations and performance scanning. |
| **Env Vars** | **Lab 11** (Adv Ops) | Lists User Environment Variables. | Shows safe handling of environment configuration. |
| **Security Alerts** | **Lab 10** (Security) | Shows alerts for Failed Logins or Antivirus status. | Fulfills the security auditing requirement. |
| **View Log** | **Lab 5** (Logging) | Opens the log file in Notepad. | Demonstrates centralized logging (`logs/system_monitor.log`). |

## 🏗️ Architecture Design (v2.0)

The project has evolved from a simple monitoring loop to a modular **Automation Platform**.

### 1. Automation Framework (`core/automation_framework.psm1`)
*   **Purpose**: Provides stability and error handling.
*   **Mechanism**: All logic is wrapped in `Invoke-SafeAction`, which handles try-catch blocks and logs errors to the Centralized Logger automatically. This fulfills Lab 5 requirements for robust scripting.

### 2. Centralized Logging (`modules/centralized_logger.psm1`)
*   **Features**:
    *   buffer rotation (keeps memory low).
    *   Severity levels (INFO, WARNING, CRITICAL).
    *   File-based logging + Console output.

### 3. Job Scheduler (`modules/job_scheduler.psm1`)
*   **Implementation**: A lightweight in-process scheduler.
*   **Loop**: The main `while` loop calls `Invoke-PendingJobs` on every tick.
*   **Jobs**: Can be registered with `Register-ScheduledJob`. Example: `SnapshotEvents` runs every 60 seconds.

### 4. Security Monitoring (`security/`)
*   **Event Log Analysis**: Uses `Get-WinEvent` with FilterHashTables for high performance (Lab 6/10).
*   **Brute Force Detection**: Queries Security Log for Event ID 4625 (Failed Logon).
*   **Firewall Checks**: Uses `Get-NetFirewallProfile`.

### 5. Diagnostics (`core/`)
*   **Services**: Checks `Get-Service` against a critical list defined in `config/settings.psd1`.
*   **Agentic Engine** (Lab 8): A rule-based system that consumes the global `$state` object and outputs text recommendations (e.g., "Scale up CPU").

## 🔄 Main Loop Logic (Enhanced)

1.  **Job Execution**: Run any due scheduled tasks.
2.  **Base Collection**: CPU, Ram, Disk (Standard).
3.  **Advanced Collection**: Security alerts, Service status (Enterprise).
4.  **AI Analysis**: The Agentic Engine reviews the collected data.
5.  **Data Push**: Everything is packaged into a huge JSON object and pushed to `dashboard/data.js`.

## 🛡️ Security Considerations
*   **Safe Execution**: The framework prevents one module for crashing the whole app.
*   **Read-Only Default**: Most modules only READ data. Action modules (like `Stop-Process`) require explicit user interaction.
