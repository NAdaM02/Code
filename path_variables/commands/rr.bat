@echo off

setlocal

if "%~1"=="" (
	for %%f in (*".rs") do (
		rustc %%f && .\%%~nf.exe
	)
) else (
    rustc %1 &&.\%~n1.exe
)

endlocal
