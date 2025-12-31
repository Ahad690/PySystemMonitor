Import-Module "$PSScriptRoot\..\core\automation_framework.psm1"

function Find-LargeFiles {
    param(
        [string]$Path = "C:\Users", 
        [int]$SizeMB = 500
    )
    
    Write-Host "Searching for files larger than ${SizeMB}MB in $Path..." -ForegroundColor Cyan
    
    # Lab 11: Advanced Ops
    Invoke-SafeAction -Name "Find-LargeFiles" -ReturnResult -Action {
        $files = Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue | 
                 Where-Object { $_.Length -gt ($SizeMB * 1MB) } |
                 Select-Object Name, Directory, @{N='SizeMB';E={[math]::Round($_.Length / 1MB, 2)}} |
                 Sort-Object SizeMB -Descending
                 
        if ($files) {
            $files | Format-Table -AutoSize
            return $files
        } else {
            Write-Host "No large files found." -ForegroundColor Gray
            return @()
        }
    }
}

Export-ModuleMember -Function Find-LargeFiles
