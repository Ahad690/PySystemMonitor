Import-Module "$PSScriptRoot\..\utils\helpers.psm1"

function Get-SystemInfo {
    $os = Get-CimInstance Win32_OperatingSystem
    $comp = Get-CimInstance Win32_ComputerSystem
    
    return @"
System Information:
  OS:       $($os.Caption)
  Version:  $($os.Version)
  Host:     $($comp.Name)
  User:     $($comp.PrimaryOwnerName)
  Boot Time: $(Get-Date $os.LastBootUpTime -Format "yyyy-MM-dd HH:mm:ss")
"@
}

Export-ModuleMember -Function Get-SystemInfo
