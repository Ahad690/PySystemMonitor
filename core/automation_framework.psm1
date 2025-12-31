Import-Module "$PSScriptRoot\..\modules\centralized_logger.psm1"

function Invoke-SafeAction {
    <#
    .SYNOPSIS
        Wraps a scriptblock in a standardized try-catch block for error handling and logging.
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,
        
        [Parameter(Mandatory=$true)]
        [scriptblock]$Action,
        
        [switch]$ReturnResult
    )
    
    try {
        # Execute the action
        $result = & $Action
        
        if ($ReturnResult) {
            return $result
        }
    }
    catch {
        $errMsg = $_.Exception.Message
        Write-Log -Level "ERROR" -Component $Name -Message "Operation failed: $errMsg"
        return $null
    }
}

function Register-Module {
    param(
        [string]$ModuleName,
        [string]$Version
    )
    
    Write-Log -Level "INFO" -Component "Framework" -Message "Registered module: $ModuleName v$Version"
}

Export-ModuleMember -Function Invoke-SafeAction, Register-Module
