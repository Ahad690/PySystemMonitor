Import-Module "$PSScriptRoot\automation_framework.psm1"
Import-Module "$PSScriptRoot\..\modules\centralized_logger.psm1"

function Get-CriticalServices {
    param([string[]]$ServiceNames)
    
    Invoke-SafeAction -Name "Get-CriticalServices" -ReturnResult -Action {
        $services = Get-Service -Name $ServiceNames -ErrorAction SilentlyContinue
        $results = @()
        
        foreach ($s in $services) {
            $status = $s.Status
            if ($status -ne 'Running') {
                Write-Log -Level "WARNING" -Component "ServiceMonitor" -Message "Critical service $($s.Name) is $status"
            }
            $results += @{
                Name = $s.Name
                DisplayName = $s.DisplayName
                Status = $status
                StartType = $s.StartType
            }
        }
        return $results
    }
}

function Restart-ServiceSafe {
    param([string]$Name)
    
    Invoke-SafeAction -Name "Restart-ServiceSafe" -ReturnResult -Action {
        $service = Get-Service -Name $Name -ErrorAction Stop
        Write-Log -Level "INFO" -Component "ServiceMonitor" -Message "Attempting to restart service $Name"
        Restart-Service -Name $Name -Force -ErrorAction Stop
        Write-Log -Level "INFO" -Component "ServiceMonitor" -Message "Service $Name restarted successfully"
        return $true
    }
}

Export-ModuleMember -Function Get-CriticalServices, Restart-ServiceSafe
