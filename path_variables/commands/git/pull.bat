@echo off

set call_dir = %cd%

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_PATH=%%i

cd %REPO_PATH%

echo ❯ Pulling at %REPO_PATH%
echo.

git checkout main

git pull

echo.
echo ❯ Pulling finished.
echo.

cd %call_dir% > nul
