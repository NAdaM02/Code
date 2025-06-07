param (
    [ArgumentCompleter({
        param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)

        $basePath = "$env:USERPROFILE\Code\path_variables\folders" # <--!!!
        
        Get-ChildItem -Path $basePath -Directory |
            Where-Object { $_.Name -like "$wordToComplete*" } |
            ForEach-Object {
                [System.Management.Automation.CompletionResult]::new(
                    $_.Name, $_.Name, 'ParameterValue', $_.Name
                )
            }
    })]
    [string]$Folder
)

Set-Location "$env:USERPROFILE\Code\path_variables\folders\$Folder" # <--!!!
Write-Host ""
