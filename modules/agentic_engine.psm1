Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

# Lab 8: "Agentic" capabilities (Simplified)
# Just a state-machine that decides actions based on system metrics

function Get-NextBestAction {
    param([hashtable]$SystemState)
    
    Invoke-SafeAction -Name "Get-NextBestAction" -ReturnResult -Action {
        $actions = @()
        
        # Rule 1: High CPU -> Recommendation
        if ($SystemState.Cpu.Current -gt 90) {
            $actions += "RECOMMENDATION: Scale up or throttle processes (CPU > 90%)"
        }
        
        # Rule 2: Low Disk Space -> Cleanup
        if ($SystemState.Disk[0].percent -gt 95) {
            $actions += "ACTION: Run Disk Cleanup (Disk > 95%)"
        }
        
        # Rule 3: Security Alert -> Locking
        if ($SystemState.Alerts | Where-Object { $_.Severity -eq 'CRITICAL' }) {
            $actions += "ACTION: Investigate Security logs immediately"
        }
        
        return $actions
    }
}

Export-ModuleMember -Function Get-NextBestAction
