@echo off

setlocal


for %%f in (*".rs") do (
	rustc %%f && .\%%~nf.exe
)

for %%f in (*".py") do (
	py %%f
)


endlocal