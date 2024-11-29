$scriptLocation = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$scriptLocation/../../folders/coder.ps1"
& "sync.bat"