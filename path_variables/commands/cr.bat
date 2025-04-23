@echo off

setlocal

for %%f in (*".pdb") do (
    del %%f
)

for %%f in (*".exe") do (
    del %%f
)
