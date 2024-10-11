@echo off

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Opening terminal with administrator privileges...
    powershell -Command "Start-Process '%comspec%' -Verb RunAs -ArgumentList '/c %~0 %*'"
    
    echo.
    exit > nul
)



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


pwsh -NoExit -Command "here.bat"
