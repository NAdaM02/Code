@echo off

setlocal


for %%f in (*".rs") do (
	code %%f
)

for %%f in (*".py") do (
	code %%f
)


endlocal