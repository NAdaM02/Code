@echo off

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_PATH=%%i

cd %REPO_PATH%

echo IN %REPO_PATH%

git checkout main

git add .

for /f "tokens=1-3 delims=:.," %%a in ("%TIME%") do (
    set "COMMIT_MSG=%%a:%%b"
)
set "COMMIT_MSG=%DATE% - %COMMIT_MSG%"

git commit -m "%COMMIT_MSG%"

echo Pulling changes from the remote repository...
git pull

echo Pushing changes...
git push

echo.
echo Upload successful.

TIMEOUT /T 1 > nul

exit
