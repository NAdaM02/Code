param (
    [ArgumentCompleter({
        param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)

        $basePath = "$env:USERPROFILE\Iskola" # <--!!!
        
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

Set-Location "$env:USERPROFILE\Iskola\$Folder" # <--!!!
Write-Host ""
