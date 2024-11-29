$scriptLocation = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$scriptLocation/../../folders/iskola.ps1"
& "sync.bat"