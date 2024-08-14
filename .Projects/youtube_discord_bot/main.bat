@echo off

call venv\Scripts\activate

pip install --upgrade -r requirements.txt

python Scripts\main.py

deactivate

pause
