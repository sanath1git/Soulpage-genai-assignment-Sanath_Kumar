@echo off
echo ========================================
echo Starting Streamlit Knowledge Bot
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run streamlit app
streamlit run app.py

pause

