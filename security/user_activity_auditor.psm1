Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

function Get-UserLoginHistory {
    param([int]$Count = 10)
    
    Invoke-SafeAction -Name "Get-UserLoginHistory" -ReturnResult -Action {
        # Event 4624 = Successful Login
        $events = Get-WinEvent -FilterHashtable @{
            LogName = 'Security'
            Id = 4624
        } -MaxEvents $Count -ErrorAction SilentlyContinue
        
        $results = @()
        foreach ($e in $events) {
            $results += @{
                Time = $e.TimeCreated.ToString("MM-dd HH:mm")
                User = $e.Properties[5].Value # TargetUserName
                Type = $e.Properties[8].Value # LogonType (2=Interactive, 3=Network, etc)
            }
        }
        return $results
    }
}

Export-ModuleMember -Function Get-UserLoginHistory
