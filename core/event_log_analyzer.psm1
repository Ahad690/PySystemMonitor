Import-Module "$PSScriptRoot\automation_framework.psm1"
Import-Module "$PSScriptRoot\..\modules\centralized_logger.psm1"

function Get-CriticalEvents {
    param([int]$Hours = 24)
    
    Invoke-SafeAction -Name "Get-CriticalEvents" -ReturnResult -Action {
        $startTime = (Get-Date).AddHours(-$Hours)
        
        # Get System and Application Errors
        $events = Get-WinEvent -FilterHashtable @{
            LogName = @('System', 'Application')
            Level = @(1, 2) # Error, Critical
            StartTime = $startTime
        } -ErrorAction SilentlyContinue
        
        if ($events) {
            Write-Log -Level "WARNING" -Component "EventLog" -Message "Found $($events.Count) critical events in last $Hours hours"
            return $events | Select-Object TimeCreated, Id, LevelDisplayName, Message, ProviderName | Sort-Object TimeCreated -Descending
        }
        return @()
    }
}

function Export-EventLogs {
    param(
        [string]$Path,
        [int]$Hours = 24
    )
    
    $events = Get-CriticalEvents -Hours $Hours
    if ($events) {
        $events | Export-Csv -Path $Path -NoTypeInformation
        Write-Log -Level "INFO" -Component "EventLog" -Message "Exported events to $Path"
    }
}

Export-ModuleMember -Function Get-CriticalEvents, Export-EventLogs
