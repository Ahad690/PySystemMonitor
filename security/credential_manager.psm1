Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

# Lab 10: Secure Credential Management
# Demonstrates secure handling of credentials using Export-Clixml and System.Security.SecureString

function Get-SecureCredential {
    param(
        [string]$TargetName,
        [switch]$Prompt
    )
    
    Invoke-SafeAction -Name "Get-SecureCredential" -ReturnResult -Action {
        $path = "$PSScriptRoot\..\config\creds_$TargetName.xml"
        
        if ($Prompt -or -not (Test-Path $path)) {
            Write-Host "Please enter credentials for $TargetName" -ForegroundColor Cyan
            $cred = Get-Credential
            $cred | Export-Clixml -Path $path
            return $cred
        } else {
            return Import-Clixml -Path $path
        }
    }
}

function Export-SecureString {
    param(
        [string]$String,
        [string]$Path
    )
    
    $secure = ConvertTo-SecureString -String $String -AsPlainText -Force
    $secure | ConvertFrom-SecureString | Set-Content -Path $Path
}

Export-ModuleMember -Function Get-SecureCredential, Export-SecureString
