@echo off
setlocal

set "fileExtension=.one"

for %%f in (*%fileExtension%) do (
	echo Opening %%f
	echo.
	start "" "%%f"
	exit /b
)

endlocal
