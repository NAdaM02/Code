@echo off
setlocal

for %%F in (*.py) do (
  if exist "%%F" (
  	echo  ***
    python "%%F"
    goto :done
  )
)

echo Error: Could not find any Python scripts (*.py) in the current folder

:done
pause