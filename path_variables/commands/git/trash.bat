@echo off

set call_dir = %cd%

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_PATH=%%i

cd %REPO_PATH%

echo ❯ Trashing and Pulling %REPO_PATH%
echo.

git restore .

git pull

echo.
echo ❯ Trashing and Pulling finished.
echo.

cd %call_dir% > nul
