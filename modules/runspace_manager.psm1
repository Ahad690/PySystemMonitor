Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

# Lab 7: Parallel Execution using Runspaces (Faster than Jobs)
# We use this to offload heavy WMI/EventLog queries without freezing the UI.

$global:RunspacePool = [runspacefactory]::CreateRunspacePool(1, 5)
$global:RunspacePool.Open()

function Start-ThreadedTask {
    param(
        [scriptblock]$ScriptBlock,
        [object[]]$Arguments = @()
    )
    
    Invoke-SafeAction -Name "Start-ThreadedTask" -ReturnResult -Action {
        $ps = [PowerShell]::Create()
        $ps.RunspacePool = $global:RunspacePool
        # AddScript -> AddParameters is better but AddArgument works for scriptblocks with param()
        $cmd = $ps.AddScript($ScriptBlock)
        
        # Add arguments individually if array
        if ($Arguments -is [array]) {
             foreach ($arg in $Arguments) {
                 $cmd.AddArgument($arg) | Out-Null
             }
        } else {
             $cmd.AddArgument($Arguments) | Out-Null
        }
        
        # Return the async handle (IAsyncResult) and the PowerShell instance to cleanup later
        return @{
            Handle = $ps.BeginInvoke()
            PowerShell = $ps
        }
    }
}

function Get-ThreadedResult {
    param([hashtable]$Task)
    
    # Non-blocking check
    if ($Task.Handle.IsCompleted) {
        try {
            $result = $Task.PowerShell.EndInvoke($Task.Handle)
            $Task.PowerShell.Dispose()
            return $result
        } catch {
            Write-Log -Level "ERROR" -Component "RunspaceManager" -Message "Thread failed: $_"
            return $null
        }
    }
    return $null
}

function Close-RunspacePool {
    if ($global:RunspacePool) {
        $global:RunspacePool.Close()
        $global:RunspacePool.Dispose()
    }
}

Export-ModuleMember -Function Start-ThreadedTask, Get-ThreadedResult, Close-RunspacePool
