@echo off

REM Check if the script is running with administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo NOT running with administrator privileges.
) else (
    echo Running with administrator privileges.
)
echo.