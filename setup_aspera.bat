@echo off

set repo_name=AlphaLabsRepo/aspera
set folder_name=aspera
set aspera_path=%USERPROFILE%\Downloads\aspera

echo This program will attempt cloning %repo_name% repo...
timeout /t 3 >nul
echo.
echo Starting...
timeout /t 1 >nul
echo.


git --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Git is not installed. Installing Git...
    powershell -Command "Start-Process 'msiexec.exe' -ArgumentList '/i https://github.com/git-for-windows/git/releases/download/v2.46.0.windows.1/Git-2.46.0-64-bit.exe /quiet' -Wait"
    if %ERRORLEVEL% neq 0 (
        echo Failed to install Git. Exiting...
        exit /b 1
    )
    echo Git installed successfully.
) else (
    echo Git is installed.
)


python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Installing Python...
    powershell -Command "Start-Process 'msiexec.exe' -ArgumentList '/i https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1' -Wait"
    if %ERRORLEVEL% neq 0 (
        echo Failed to install Python. Exiting...
        exit /b 1
    )
    echo Python installed successfully.
) else (
    echo Python is installed.
)


pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Pip is not installed. Installing Pip...
    python -m ensurepip --upgrade
    if %ERRORLEVEL% neq 0 (
        echo Failed to install Pip. Exiting...
        exit /b 1
    )
    echo Pip installed successfully.
) else (
    echo Pip is installed.
)

echo.
echo All required software installed.
echo.




if exist "%aspera_path%" (
	rmdir /s /q "%aspera_path%"
	echo Aspera folder deleted.
	echo.
)

echo Cloning the repository...
echo.

git clone https://github.com/%repo_name%.git
IF %ERRORLEVEL% NEQ 0 (
	echo Failed to clone the repository. Please check the repository URL and your internet connection.
	exit /b 1
)

echo Repository cloned successfully.
echo.




cd %aspera_path%\Backend\

echo.
set /p OPENAI_API_KEY=Please enter your OPENAI_API_KEY: 
echo. 

del %aspera_path%\Backend\.env.example

(
echo OPENAI_API_KEY="%OPENAI_API_KEY%"
echo GEMINI_API_KEY="..."
) > "%aspera_path%\backend\.env"

echo .env file has been created with the provided API key.
echo.




python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
	echo Python is not installed. Attempting to install Python...
	choco install python
	IF %ERRORLEVEL% NEQ 0 (
		echo Failed to install python. Please try to install Python manually.
		exit /b 1
	)
)


pip install -r %aspera_path%\backend\requirements.txt

IF %ERRORLEVEL% NEQ 0 (
	echo pip command not found. Please try adding pip to PATH manually.
	exit /b 1
)

(
	echo @echo off
	echo python .\backend\main.py
) > "%aspera_path%\RUN.bat"




echo RUN.bat file has been created.
echo.
echo.
echo Setup successfull.
echo You can run the program by running the created RUN.bat file located in folder:
echo "Downloads/%folder_name%"

pause
