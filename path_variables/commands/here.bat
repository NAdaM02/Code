@echo off

for /f "tokens=1-3 delims=:.," %%a in ("%TIME%") do (
    set "start_time=%%a:%%b/%%c"
)

cls
echo # Terminal at %CD%
echo ............
echo  %start_time%
echo      %DATE%
echo ............
echo.

pwsh7 -noexit -Command "& \"%temp%\prompt.ps1\"; $host.UI.RawUI.WindowTitle = 'Terminal @ %CD%'"
