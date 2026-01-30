@echo off
echo ========================================
echo Conversational Knowledge Bot - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo [1/4] Python found!
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment and install dependencies
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Setup .env file
echo [4/4] Setting up environment variables...
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your Groq API key!
    echo Get your free API key from: https://console.groq.com/
    echo.
) else (
    echo .env file already exists.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Get your free Groq API key from: https://console.groq.com/
echo 2. Edit .env file and add your API key
echo 3. Run the bot:
echo    - Streamlit UI: streamlit run app.py
echo    - Command line: python main.py
echo.
echo Press any key to exit...
pause >nul

