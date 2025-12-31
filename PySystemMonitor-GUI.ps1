# PySystemMonitor-PS GUI Edition
# Fallback GUI for demonstration - ALL LABS (5-11)
# Compatible with Windows PowerShell 5.1

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$ScriptRoot = $PSScriptRoot

# Import modules
Import-Module "$ScriptRoot\core\cpu_monitor.psm1" -ErrorAction SilentlyContinue
Import-Module "$ScriptRoot\core\memory_monitor.psm1" -ErrorAction SilentlyContinue
Import-Module "$ScriptRoot\core\disk_monitor.psm1" -ErrorAction SilentlyContinue
Import-Module "$ScriptRoot\core\network_monitor.psm1" -ErrorAction SilentlyContinue
Import-Module "$ScriptRoot\core\process_manager.psm1" -ErrorAction SilentlyContinue
Import-Module "$ScriptRoot\core\service_monitor.psm1" -ErrorAction SilentlyContinue

$Config = Import-PowerShellDataFile "$ScriptRoot\config\settings.psd1"

# Create Form
$form = New-Object System.Windows.Forms.Form
$form.Text = "PySystemMonitor-PS Enterprise (Labs 5-11)"
$form.Size = New-Object System.Drawing.Size(850, 700)
$form.StartPosition = "CenterScreen"
$form.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$form.ForeColor = [System.Drawing.Color]::White

# Title Label
$titleLabel = New-Object System.Windows.Forms.Label
$titleLabel.Text = "PySystemMonitor-PS Enterprise Edition"
$titleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
$titleLabel.ForeColor = [System.Drawing.Color]::Cyan
$titleLabel.Location = New-Object System.Drawing.Point(20, 10)
$titleLabel.Size = New-Object System.Drawing.Size(500, 30)
$form.Controls.Add($titleLabel)

# CPU Label
$cpuLabel = New-Object System.Windows.Forms.Label
$cpuLabel.Text = "CPU: Loading..."
$cpuLabel.Font = New-Object System.Drawing.Font("Consolas", 12)
$cpuLabel.Location = New-Object System.Drawing.Point(20, 50)
$cpuLabel.Size = New-Object System.Drawing.Size(350, 25)
$form.Controls.Add($cpuLabel)

# CPU Progress Bar
$cpuBar = New-Object System.Windows.Forms.ProgressBar
$cpuBar.Location = New-Object System.Drawing.Point(20, 75)
$cpuBar.Size = New-Object System.Drawing.Size(350, 20)
$form.Controls.Add($cpuBar)

# Memory Label
$memLabel = New-Object System.Windows.Forms.Label
$memLabel.Text = "Memory: Loading..."
$memLabel.Font = New-Object System.Drawing.Font("Consolas", 12)
$memLabel.Location = New-Object System.Drawing.Point(420, 50)
$memLabel.Size = New-Object System.Drawing.Size(400, 25)
$form.Controls.Add($memLabel)

# Memory Progress Bar
$memBar = New-Object System.Windows.Forms.ProgressBar
$memBar.Location = New-Object System.Drawing.Point(420, 75)
$memBar.Size = New-Object System.Drawing.Size(390, 20)
$form.Controls.Add($memBar)

# Disk & Network Labels
$diskLabel = New-Object System.Windows.Forms.Label
$diskLabel.Text = "Disk: Loading..."
$diskLabel.Font = New-Object System.Drawing.Font("Consolas", 11)
$diskLabel.Location = New-Object System.Drawing.Point(20, 105)
$diskLabel.Size = New-Object System.Drawing.Size(350, 20)
$form.Controls.Add($diskLabel)

$netLabel = New-Object System.Windows.Forms.Label
$netLabel.Text = "Network: Loading..."
$netLabel.Font = New-Object System.Drawing.Font("Consolas", 11)
$netLabel.Location = New-Object System.Drawing.Point(420, 105)
$netLabel.Size = New-Object System.Drawing.Size(400, 20)
$form.Controls.Add($netLabel)

# Services Group (Lab 6)
$svcGroup = New-Object System.Windows.Forms.GroupBox
$svcGroup.Text = "Critical Services (Lab 6)"
$svcGroup.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$svcGroup.ForeColor = [System.Drawing.Color]::Cyan
$svcGroup.Location = New-Object System.Drawing.Point(20, 135)
$svcGroup.Size = New-Object System.Drawing.Size(350, 130)
$form.Controls.Add($svcGroup)

$svcList = New-Object System.Windows.Forms.ListBox
$svcList.Location = New-Object System.Drawing.Point(10, 20)
$svcList.Size = New-Object System.Drawing.Size(330, 100)
$svcList.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
$svcList.ForeColor = [System.Drawing.Color]::LightGreen
$svcList.Font = New-Object System.Drawing.Font("Consolas", 10)
$svcGroup.Controls.Add($svcList)

# Processes Group
$procGroup = New-Object System.Windows.Forms.GroupBox
$procGroup.Text = "Top Processes"
$procGroup.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$procGroup.ForeColor = [System.Drawing.Color]::Cyan
$procGroup.Location = New-Object System.Drawing.Point(420, 135)
$procGroup.Size = New-Object System.Drawing.Size(390, 130)
$form.Controls.Add($procGroup)

$procList = New-Object System.Windows.Forms.ListBox
$procList.Location = New-Object System.Drawing.Point(10, 20)
$procList.Size = New-Object System.Drawing.Size(280, 100)
$procList.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
$procList.ForeColor = [System.Drawing.Color]::White
$procList.Font = New-Object System.Drawing.Font("Consolas", 10)
$procGroup.Controls.Add($procList)

# Kill Process Button
$killBtn = New-Object System.Windows.Forms.Button
$killBtn.Text = "Kill"
$killBtn.Location = New-Object System.Drawing.Point(300, 20)
$killBtn.Size = New-Object System.Drawing.Size(80, 30)
$killBtn.BackColor = [System.Drawing.Color]::DarkRed
$killBtn.ForeColor = [System.Drawing.Color]::White
$killBtn.Add_Click({
    $selected = $procList.SelectedItem
    if ($selected) {
        $processId = ($selected -split '\s+')[0]
        try {
            Stop-Process -Id $processId -Force -ErrorAction Stop
            [System.Windows.Forms.MessageBox]::Show("Process $processId terminated!", "Success")
        } catch {
            [System.Windows.Forms.MessageBox]::Show("Failed: $_", "Error")
        }
    }
})
$procGroup.Controls.Add($killBtn)

# ============ LAB 7: Parallel Execution ============
$lab7Group = New-Object System.Windows.Forms.GroupBox
$lab7Group.Text = "Parallel Execution (Lab 7)"
$lab7Group.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$lab7Group.ForeColor = [System.Drawing.Color]::Magenta
$lab7Group.Location = New-Object System.Drawing.Point(20, 275)
$lab7Group.Size = New-Object System.Drawing.Size(350, 100)
$form.Controls.Add($lab7Group)

$lab7Status = New-Object System.Windows.Forms.Label
$lab7Status.Text = "Background jobs: Ready"
$lab7Status.Font = New-Object System.Drawing.Font("Consolas", 9)
$lab7Status.Location = New-Object System.Drawing.Point(10, 20)
$lab7Status.Size = New-Object System.Drawing.Size(330, 20)
$lab7Group.Controls.Add($lab7Status)

# We use this to track active jobs by ID
$global:MyJobId = $null

$runJobBtn = New-Object System.Windows.Forms.Button
$runJobBtn.Text = "Start Background Job"
$runJobBtn.Location = New-Object System.Drawing.Point(10, 45)
$runJobBtn.Size = New-Object System.Drawing.Size(150, 30)
$runJobBtn.BackColor = [System.Drawing.Color]::DarkMagenta
$runJobBtn.ForeColor = [System.Drawing.Color]::White
$runJobBtn.Add_Click({
    $job = Start-Job -ScriptBlock {
        Start-Sleep -Seconds 3
        return "Job completed at $(Get-Date -Format 'HH:mm:ss')"
    }
    $global:MyJobId = $job.Id
    $lab7Status.Text = "Job $($job.Id) running..."
    $lab7Status.ForeColor = [System.Drawing.Color]::Yellow
})
$lab7Group.Controls.Add($runJobBtn)

$parallelBtn = New-Object System.Windows.Forms.Button
$parallelBtn.Text = "Simulate Parallel"
$parallelBtn.Location = New-Object System.Drawing.Point(170, 45)
$parallelBtn.Size = New-Object System.Drawing.Size(120, 30)
$parallelBtn.BackColor = [System.Drawing.Color]::DarkMagenta
$parallelBtn.ForeColor = [System.Drawing.Color]::White
$parallelBtn.Add_Click({
    $lab7Status.Text = "Running 3 tasks..."
    $lab7Status.ForeColor = [System.Drawing.Color]::Yellow
    # Simple simulation to avoid PS version issues
    $jobs = 1..3 | ForEach-Object {
        Start-Job -ScriptBlock { Start-Sleep -Seconds 1; return "Done" }
    }
    # Don't wait, just let timer clean them up or update status
    $lab7Status.Text = "Started 3 jobs ($($jobs.Id -join ','))"
})
$lab7Group.Controls.Add($parallelBtn)

# ============ LAB 8: Agentic Insights ============
$lab8Group = New-Object System.Windows.Forms.GroupBox
$lab8Group.Text = "Agentic Insights (Lab 8)"
$lab8Group.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$lab8Group.ForeColor = [System.Drawing.Color]::Orange
$lab8Group.Location = New-Object System.Drawing.Point(420, 275)
$lab8Group.Size = New-Object System.Drawing.Size(390, 100)
$form.Controls.Add($lab8Group)

$insightsList = New-Object System.Windows.Forms.ListBox
$insightsList.Location = New-Object System.Drawing.Point(10, 20)
$insightsList.Size = New-Object System.Drawing.Size(370, 70)
$insightsList.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
$insightsList.ForeColor = [System.Drawing.Color]::Orange
$insightsList.Font = New-Object System.Drawing.Font("Consolas", 9)
$lab8Group.Controls.Add($insightsList)

# ============ LAB 9 & 11: Automation ============
$autoGroup = New-Object System.Windows.Forms.GroupBox
$autoGroup.Text = "Automation Scripts (Lab 9 & 11)"
$autoGroup.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$autoGroup.ForeColor = [System.Drawing.Color]::LightBlue
$autoGroup.Location = New-Object System.Drawing.Point(20, 385)
$autoGroup.Size = New-Object System.Drawing.Size(350, 80)
$form.Controls.Add($autoGroup)

$cleanupBtn = New-Object System.Windows.Forms.Button
$cleanupBtn.Text = "Disk Cleanup"
$cleanupBtn.Location = New-Object System.Drawing.Point(10, 25)
$cleanupBtn.Size = New-Object System.Drawing.Size(100, 35)
$cleanupBtn.BackColor = [System.Drawing.Color]::Teal
$cleanupBtn.ForeColor = [System.Drawing.Color]::White
$cleanupBtn.Add_Click({
    [System.Windows.Forms.MessageBox]::Show("Disk Cleanup Simulation Complete!`n`nTemp files would be cleared.", "Lab 9")
})
$autoGroup.Controls.Add($cleanupBtn)

$global:LargeFileJobId = $null

$largeBtn = New-Object System.Windows.Forms.Button
$largeBtn.Text = "Large Files"
$largeBtn.Location = New-Object System.Drawing.Point(120, 25)
$largeBtn.Size = New-Object System.Drawing.Size(100, 35)
$largeBtn.BackColor = [System.Drawing.Color]::Teal
$largeBtn.ForeColor = [System.Drawing.Color]::White
$largeBtn.Add_Click({
    $alertList.Items.Clear()
    $alertList.Items.Add("Searching (>100MB)...")
    
    $j = Start-Job -ScriptBlock {
        Get-ChildItem -Path "C:\Users" -Recurse -File -ErrorAction SilentlyContinue | 
             Where-Object { $_.Length -gt 100MB } | 
             Select-Object -First 5 Name, @{N='MB';E={[math]::Round($_.Length/1MB,1)}}
    }
    $global:LargeFileJobId = $j.Id
})
$autoGroup.Controls.Add($largeBtn)

$envBtn = New-Object System.Windows.Forms.Button
$envBtn.Text = "Env Vars"
$envBtn.Location = New-Object System.Drawing.Point(230, 25)
$envBtn.Size = New-Object System.Drawing.Size(100, 35)
$envBtn.BackColor = [System.Drawing.Color]::Teal
$envBtn.ForeColor = [System.Drawing.Color]::White
$envBtn.Add_Click({
    $envVars = [Environment]::GetEnvironmentVariables("User")
    $msg = "User Environment Variables:`n`n"
    $envVars.Keys | Select-Object -First 10 | ForEach-Object { $msg += "$_`n" }
    [System.Windows.Forms.MessageBox]::Show($msg, "Lab 11: Environment Manager")
})
$autoGroup.Controls.Add($envBtn)

# ============ LAB 10: Security ============
$alertGroup = New-Object System.Windows.Forms.GroupBox
$alertGroup.Text = "Security Alerts (Lab 10)"
$alertGroup.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$alertGroup.ForeColor = [System.Drawing.Color]::Red
$alertGroup.Location = New-Object System.Drawing.Point(420, 385)
$alertGroup.Size = New-Object System.Drawing.Size(390, 150)
$form.Controls.Add($alertGroup)

$alertList = New-Object System.Windows.Forms.ListBox
$alertList.Location = New-Object System.Drawing.Point(10, 20)
$alertList.Size = New-Object System.Drawing.Size(370, 120)
$alertList.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
$alertList.ForeColor = [System.Drawing.Color]::Yellow
$alertList.Font = New-Object System.Drawing.Font("Consolas", 9)
$alertGroup.Controls.Add($alertList)

# ============ LAB 5: Logging ============
$logGroup = New-Object System.Windows.Forms.GroupBox
$logGroup.Text = "Centralized Logging (Lab 5)"
$logGroup.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$logGroup.ForeColor = [System.Drawing.Color]::Gray
$logGroup.Location = New-Object System.Drawing.Point(20, 475)
$logGroup.Size = New-Object System.Drawing.Size(350, 60)
$form.Controls.Add($logGroup)

$logLabel = New-Object System.Windows.Forms.Label
$logLabel.Text = "Logs written to: logs/system_monitor.log"
$logLabel.Font = New-Object System.Drawing.Font("Consolas", 9)
$logLabel.Location = New-Object System.Drawing.Point(10, 20)
$logLabel.Size = New-Object System.Drawing.Size(330, 20)
$logGroup.Controls.Add($logLabel)

$viewLogBtn = New-Object System.Windows.Forms.Button
$viewLogBtn.Text = "View Log"
$viewLogBtn.Location = New-Object System.Drawing.Point(250, 35)
$viewLogBtn.Size = New-Object System.Drawing.Size(80, 20)
$viewLogBtn.Add_Click({
    $logPath = "$ScriptRoot\logs\system_monitor.log"
    if (Test-Path $logPath) {
        Start-Process notepad.exe -ArgumentList $logPath
    } else {
        [System.Windows.Forms.MessageBox]::Show("Log file not found", "Info")
    }
})
$logGroup.Controls.Add($viewLogBtn)

# Status Label
$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Text = "Status: Initializing..."
$statusLabel.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$statusLabel.ForeColor = [System.Drawing.Color]::LightGreen
$statusLabel.Location = New-Object System.Drawing.Point(20, 545)
$statusLabel.Size = New-Object System.Drawing.Size(790, 20)
$form.Controls.Add($statusLabel)

# Timer for updates
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 2000

$timer.Add_Tick({
    try {
        # ---- Job Management (Fixed Scope) ----
        if ($global:MyJobId) {
            $j = Get-Job -Id $global:MyJobId -ErrorAction SilentlyContinue
            if ($j -and $j.State -eq 'Completed') {
                 $res = Receive-Job -Job $j -Keep
                 $lab7Status.Text = "Result: $res"
                 $lab7Status.ForeColor = [System.Drawing.Color]::LightGreen
                 Remove-Job -Job $j -Force
                 $global:MyJobId = $null
            }
        }
        
        if ($global:LargeFileJobId) {
            $j = Get-Job -Id $global:LargeFileJobId -ErrorAction SilentlyContinue
            if ($j -and $j.State -eq 'Completed') {
                $files = Receive-Job -Job $j -Keep
                $alertList.Items.Clear()
                if ($files) {
                    foreach ($f in $files) { $alertList.Items.Add("$($f.Name) - $($f.MB) MB") }
                } else {
                    $alertList.Items.Add("No files > 100MB found")
                }
                Remove-Job -Job $j -Force
                $global:LargeFileJobId = $null
            }
        }

        # Update CPU
        $cpu = Get-CpuUsage
        $cpuLabel.Text = "CPU: $cpu%"
        $cpuBar.Value = [Math]::Min(100, [int]$cpu)
        
        # Update Memory
        $mem = Get-MemoryUsage
        $memLabel.Text = "Memory: $($mem.percent)% ($($mem.used) / $($mem.total))"
        $memBar.Value = [Math]::Min(100, [int]$mem.percent)
        
        # Update Disk
        $disk = Get-DiskUsage
        if ($disk.Count -gt 0) {
            $diskLabel.Text = "Disk C: $($disk[0].percent)% used ($($disk[0].free) free)"
        }
        
        # Update Network
        $net = Get-NetworkStats
        $netLabel.Text = "Net: Up $($net.upload)/s Down $($net.download)/s"
        
        # Update Services (Lab 6)
        $svcList.Items.Clear()
        $services = Get-CriticalServices -ServiceNames $Config.CriticalServices
        foreach ($s in $services) {
            $statusText = if ($s.Status -eq 4 -or $s.Status -eq 'Running') { "Running" } else { "Stopped" }
            $tag = if ($statusText -eq 'Running') { "[OK]" } else { "[!!]" }
            $svcList.Items.Add("$tag $($s.Name) ($statusText)")
        }
        
        # Update Processes
        $procList.Items.Clear()
        $procs = Get-TopProcesses -Count 5
        foreach ($p in $procs) {
            $procList.Items.Add("$($p.pid) $($p.name) CPU:$([math]::Round($p.cpu_percent,1))")
        }
        
        # Update Agentic Insights (Lab 8)
        $insightsList.Items.Clear()
        if ($cpu -gt 80) {
            $insightsList.Items.Add("! High CPU - Consider scaling")
        }
        if ($disk.Count -gt 0 -and $disk[0].percent -gt 90) {
            $insightsList.Items.Add("! Low Disk Space - Run cleanup")
        }
        if ($insightsList.Items.Count -eq 0) {
            $insightsList.Items.Add("System healthy")
            $insightsList.ForeColor = [System.Drawing.Color]::LightGreen
        } else {
            $insightsList.ForeColor = [System.Drawing.Color]::Orange
        }
        
        $statusLabel.Text = "Status: Running | Labs: 5-11 | Last update: $(Get-Date -Format 'HH:mm:ss')"
    } catch {
        # Ignore minor UI update errors
    }
})

$timer.Start()
$form.Add_FormClosing({ 
    $timer.Stop()
    Get-Job | Remove-Job -Force -ErrorAction SilentlyContinue
})

[void]$form.ShowDialog()
