Import-Module "$PSScriptRoot\..\utils\helpers.psm1"

function Write-Log {
    param(
        [string]$Path,
        [string]$Level,
        [string]$Message
    )
    
    $timestamp = Get-Timestamp
    $line = "[$timestamp] [$Level] $Message"
    
    # Ensure directory exists
    $dir = Split-Path $Path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    
    Add-Content -Path $Path -Value $line
}

function Export-To-Web {
    param(
        [string]$Path,
        [hashtable]$Data
    )
    
    # Needs to be valid JS for JSONP/Script tag
    # window.updateData({...})
    $json = $Data | ConvertTo-Json -Depth 10 -Compress
    $content = "window.updateData($json);"
    
    Set-Content -Path $Path -Value $content
}


Export-ModuleMember -Function Write-Log, Export-To-Web
