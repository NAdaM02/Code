@echo off

rem Add all files to the staging area
git add --all

rem Commit the changes with the current date and time as the message
set COMMIT_MSG=%DATE% - %TIME%
git commit -m "%COMMIT_MSG%"

rem Update the commit message for all files
git commit --amend -m "%COMMIT_MSG%"

echo Pulling changes from the remote repository...
git pull --tags origin main

echo Pushing changes...
git push --force --quiet

echo.
echo Upload successful.

rem Remove the pause command if you don't want to wait for user input

timeout /t 3

exit
