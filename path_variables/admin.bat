@echo off

REM Check if the script is running with administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Opening terminal with administrator privileges...
    powershell -Command "Start-Process '%comspec%' -Verb RunAs -ArgumentList '/c %~0 %*'"
    
    echo.
    exit > nul
)

REM Script continues here if running as administrator
REM Add your commands that require elevated privileges below
for /f "tokens=1-3 delims=:.," %%a in ("%TIME%") do (
    set "start_time=%%a:%%b:%%c"
)

cls
echo # Admin at %CD%
echo ............
echo  %start_time%
echo      %DATE%
echo ............
echo.

echo function global:prompt { $prompting = ""; $path = (Get-Location).Path.Replace($env:USERPROFILE, '~'); return "$prompting$path> "; } > "%temp%\prompt.ps1"
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoExit -Command "$host.UI.RawUI.WindowTitle = 'Admin @ %CD%'; . '%temp%\prompt.ps1'"