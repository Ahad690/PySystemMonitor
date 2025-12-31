Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

# Lab 9: Multi-Script Automation Controller
# Manages execution of standalone automation scripts

function Show-AutomationMenu {
    Clear-Host
    Write-Host "--- AUTOMATION CONTROLLER (Lab 9) ---" -ForegroundColor Cyan
    Write-Host "1. Run Disk Cleanup"
    Write-Host "2. Find Large Files (>500MB)"
    Write-Host "3. Reset Network Adapter"
    Write-Host "4. Audit Admin Group Users"
    Write-Host "B. Back to Dashboard"
    Write-Host "-------------------------------------"
    
    $choice = Read-Host "Select Task"
    return $choice
}

function Invoke-AutomationTask {
    param([string]$TaskID)
    
    switch ($TaskID) {
        "1" { Invoke-DiskCleanup }
        "2" { 
            # Check if command exists, otherwise warn
            if (Get-Command Find-LargeFiles -ErrorAction SilentlyContinue) {
                Find-LargeFiles -Path "C:\" -SizeMB 500 
            } else {
                Write-Warning "Find-LargeFiles command not found. Ensure disk_management_automation.psm1 is loaded."
            }
        }
        "3" { Reset-NetworkStack }
        "4" { Audit-AdminGroup }
        "B" { return }
        Default { Write-Warning "Unknown Task ID"; Start-Sleep -Seconds 1 }
    }
    
    if ($TaskID -ne "B") {
        Write-Host "`nPress any key to continue..."
        [Console]::ReadKey() | Out-Null
    }
}

# Placeholder implementations
function Invoke-DiskCleanup {
    Write-Host "Running Disk Cleanup Simulation..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    Write-Host "Temp files cleared." -ForegroundColor Green
}

function Reset-NetworkStack {
    Write-Host "Resetting Network Stack..." -ForegroundColor Yellow
    Start-Sleep -Seconds 1
    Write-Host "DNS Flushed." -ForegroundColor Green
}

function Audit-AdminGroup {
    Write-Host "Auditing Administrators Group..." -ForegroundColor Yellow
    # Using generic error handling just in case
    try {
        Get-LocalGroupMember -Group "Administrators" | Format-Table
    } catch {
        Write-Warning "Could not query Admins group: $_"
    }
}

Export-ModuleMember -Function Show-AutomationMenu, Invoke-AutomationTask, Invoke-DiskCleanup
