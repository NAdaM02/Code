@echo off

set call_dir = %cd%

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_PATH=%%i

cd %REPO_PATH%

echo Commiting at %REPO_PATH%
echo.

git checkout main

set /p COMMIT_MSG="commit message: "
echo.

if "%COMMIT_MSG%"=="" (
    for /f "tokens=1-3 delims=:.," %%a in ("%TIME%") do (
        set "COMMIT_MSG=%%a:%%b"
    )
    set "COMMIT_MSG=%DATE% - %COMMIT_MSG%"
)

git commit -m "%COMMIT_MSG%"

echo.
echo Commiting finished.
echo.

cd %call_dir% > nul
