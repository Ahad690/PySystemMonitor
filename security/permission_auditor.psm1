Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

# Lab 10: Permission Auditor
# Checks ACLs for sensitive folders

function Get-FolderAcl {
    param([string]$Path)
    
    Invoke-SafeAction -Name "Get-FolderAcl" -ReturnResult -Action {
        $acl = Get-Acl -Path $Path
        return $acl.Access | Select-Object IdentityReference, FileSystemRights, AccessControlType
    }
}

function Audit-SensitivePaths {
    param([string[]]$Paths = @("C:\Windows", "C:\Users"))
    
    $results = @()
    foreach ($p in $Paths) {
        if (Test-Path $p) {
            $acls = Get-FolderAcl -Path $p
            # Check for generic "Everyone" full control (Security Risk)
            $risk = $acls | Where-Object { $_.IdentityReference -match "Everyone" -and $_.FileSystemRights -match "FullControl" }
            
            $results += @{
                Path = $p
                Risks = if ($risk) { "CRITICAL: Everyone has Full Control" } else { "Secure" }
            }
        }
    }
    return $results
}

Export-ModuleMember -Function Get-FolderAcl, Audit-SensitivePaths
