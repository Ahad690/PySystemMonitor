Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

$global:ScheduledJobs = @()

function Register-ScheduledJob {
    param(
        [string]$Name,
        [scriptblock]$Action,
        [int]$IntervalSeconds
    )
    
    Invoke-SafeAction -Name "Register-ScheduledJob" -ReturnResult -Action {
        $job = @{
            Name = $Name
            Action = $Action
            Interval = $IntervalSeconds
            LastRun = [DateTime]::MinValue
            NextRun = (Get-Date).AddSeconds($IntervalSeconds)
            Enabled = $true
        }
        $global:ScheduledJobs += $job
        Write-Log -Level "INFO" -Component "Scheduler" -Message "Registered job: $Name (Interval: ${IntervalSeconds}s)"
        return $job
    }
}

function Invoke-PendingJobs {
    Invoke-SafeAction -Name "Invoke-PendingJobs" -ReturnResult -Action {
        $now = Get-Date
        foreach ($job in $global:ScheduledJobs) {
            if ($job.Enabled -and $now -ge $job.NextRun) {
                Write-Log -Level "DEBUG" -Component "Scheduler" -Message "Running job: $($job.Name)"
                
                # Run the job
                try {
                    & $job.Action
                } catch {
                    Write-Log -Level "ERROR" -Component "Scheduler" -Message "Job $($job.Name) failed: $_"
                }
                
                # Schedule next run
                $job.LastRun = $now
                $job.NextRun = $now.AddSeconds($job.Interval)
            }
        }
    }
}

function Get-JobStatus {
    return $global:ScheduledJobs | Select-Object Name, LastRun, NextRun, Interval, Enabled
}

Export-ModuleMember -Function Register-ScheduledJob, Invoke-PendingJobs, Get-JobStatus
