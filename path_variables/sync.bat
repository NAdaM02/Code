@echo off

set call_dir = %cd%

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_PATH=%%i

cd %REPO_PATH%

echo Syncing at %REPO_PATH%
echo.


git checkout main > nul

git add .

for /f "tokens=1-3 delims=:.," %%a in ("%TIME%") do (
    set "COMMIT_MSG=%%a:%%b"
)
set "COMMIT_MSG=%DATE% - %COMMIT_MSG%"

git commit -m "%COMMIT_MSG%"

echo.
echo PULL-ing changes...
git pull

echo.
echo PUSH-ing changes...
git push

echo.
echo Syncing finished.
echo.

cd %call_dir% > nul
