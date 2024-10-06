@echo off

call venv\Scripts\activate

pip install --upgrade -r requirements.txt

python main.py

deactivate

pause
