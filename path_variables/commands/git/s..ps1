&scriptLocation = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$PSScriptRoot/../../folders/coder.ps1"
& "sync.bat"
& "$scriptLocation/../../folders/iskola.ps1"
& "sync.bat"