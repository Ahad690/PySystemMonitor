Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

# In a real scenario, we might use Start-Job or PoshRSJob.
# For this lab, we wrap PowerShell Background Jobs.

function Start-BackgroundMonitor {
    param(
        [string]$Name,
        [scriptblock]$ScriptBlock
    )
    
    Invoke-SafeAction -Name "Start-BackgroundMonitor" -ReturnResult -Action {
        Write-Log -Level "INFO" -Component "JobManager" -Message "Starting background job: $Name"
        return Start-Job -Name $Name -ScriptBlock $ScriptBlock
    }
}

function Get-JobResults {
    param([string]$Name)
    
    Invoke-SafeAction -Name "Get-JobResults" -ReturnResult -Action {
        $job = Get-Job -Name $Name -ErrorAction SilentlyContinue
        if ($job) {
            return Receive-Job -Job $job -Keep
        }
        return $null
    }
}

function Cleanup-Jobs {
    Get-Job | Where-Object { $_.State -eq 'Completed' -or $_.State -eq 'Failed' } | Remove-Job
}

Export-ModuleMember -Function Start-BackgroundMonitor, Get-JobResults, Cleanup-Jobs
