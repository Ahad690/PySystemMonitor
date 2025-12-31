Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"
Import-Module "$PSScriptRoot\..\modules\centralized_logger.psm1"

function Get-SecurityAlerts {
    param([int]$FailedLoginThreshold = 5)
    
    $alerts = @()
    
    try {
        # Check Firewall Status
        try {
            $firewall = Get-NetFirewallProfile -Profile Domain,Public,Private -ErrorAction Stop
            foreach ($fw in $firewall) {
                if ($fw.Enabled -eq $false) {
                    $alerts += @{
                        Severity = "CRITICAL"
                        Message = "Firewall disabled on profile: $($fw.Name)"
                        Timestamp = Get-Date -Format "HH:mm:ss"
                    }
                }
            }
        } catch {
            Write-Log -Level "DEBUG" -Component "Security" -Message "Could not check firewall status"
        }
        
        # Check Antivirus (Generic WMI check)
        try {
            $av = Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct -ErrorAction Stop
            if (-not $av) {
                $alerts += @{
                    Severity = "WARNING"
                    Message = "No Antivirus product detected"
                    Timestamp = Get-Date -Format "HH:mm:ss"
                }
            }
        } catch {
            # Silently ignore if we can't check AV status
            Write-Log -Level "DEBUG" -Component "Security" -Message "Could not check AV status"
        }
        
        # Check Failed Logins (Event 4625) - This requires admin rights
        try {
            $failedLogins = @(Get-WinEvent -FilterHashtable @{
                LogName = 'Security'
                Id = 4625
                StartTime = (Get-Date).AddHours(-1)
            } -MaxEvents 100 -ErrorAction Stop)
            
            if ($failedLogins.Count -ge $FailedLoginThreshold) {
                $alerts += @{
                    Severity = "CRITICAL"
                    Message = "High failed login attempts detected ($($failedLogins.Count)) in last hour"
                    Timestamp = Get-Date -Format "HH:mm:ss"
                }
                Write-Log -Level "CRITICAL" -Component "Security" -Message "Brute force suspected: $($failedLogins.Count) failed logins"
            }
        } catch {
            # Failed to query Security log - likely permission issue or no events
            # This is expected on non-admin accounts, so we just skip it
            Write-Log -Level "DEBUG" -Component "Security" -Message "Could not query Security event log (may need admin rights)"
        }
        
        return $alerts
        
    } catch {
        Write-Log -Level "ERROR" -Component "Get-SecurityAlerts" -Message "Operation failed: $($_.Exception.Message)"
        return @()
    }
}

function Get-ComplianceStatus {
    # Lab 10: Audit/Governance
    return @{
        Firewall = (Get-NetFirewallProfile -Profile Public).Enabled
        UAC = (Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System).EnableLUA -eq 1
        SecureBoot = $true # Placeholder for complex secure boot check
    }
}

Export-ModuleMember -Function Get-SecurityAlerts, Get-ComplianceStatus
