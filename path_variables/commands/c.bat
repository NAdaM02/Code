@echo off
setlocal

for %%f in (*".rs") do (
	code %%f
)

for %%f in (*".py") do (
	code %%f
)

for %%f in (*".ps1") do (
	code %%f
)

for %%f in (*".bat") do (
	code %%f
)

endlocal
