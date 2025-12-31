Import-Module "$PSScriptRoot\automation_framework.psm1"
Import-Module "$PSScriptRoot\..\modules\centralized_logger.psm1"

function Get-EnvironmentVariables {
    param([string]$Scope = "Machine")
    
    Invoke-SafeAction -Name "Get-EnvironmentVariables" -ReturnResult -Action {
        return [Environment]::GetEnvironmentVariables($Scope)
    }
}

function Set-EnvironmentVariableSafe {
    param(
        [string]$Name,
        [string]$Value,
        [string]$Scope = "User"
    )
    
    Invoke-SafeAction -Name "Set-EnvironmentVariableSafe" -ReturnResult -Action {
        [Environment]::SetEnvironmentVariable($Name, $Value, $Scope)
        Write-Log -Level "INFO" -Component "EnvManager" -Message "Set env var $Name in $Scope scope"
        return $true
    }
}

Export-ModuleMember -Function Get-EnvironmentVariables, Set-EnvironmentVariableSafe
