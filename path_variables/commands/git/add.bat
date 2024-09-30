@echo off

set call_dir = %cd%

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_PATH=%%i

cd %REPO_PATH%

echo Adding all to %REPO_PATH%
echo.

git checkout main > nul

git add *

echo.
echo Adding finished.
echo.

cd %call_dir% > nul
