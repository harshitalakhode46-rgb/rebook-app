@echo off
REM ReBook Application Startup Script for Windows
REM This script starts both backend and frontend servers

echo ========================================
echo Starting ReBook Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo Error: Virtual environment not found!
    echo Please run setup first:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo   python setup.py
    pause
    exit /b 1
)

REM Check if database exists
if not exist "backend\rebook.db" (
    echo Warning: Database not found!
    echo Running setup script...
    cd backend
    call venv\Scripts\activate
    python setup.py
    cd ..
)

echo Starting Backend Server...
start "ReBook Backend" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn main:app --reload"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "ReBook Frontend" cmd /k "cd frontend && python -m http.server 8080"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo ReBook is now running!
echo ========================================
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:8080
echo.
echo Press any key to stop all servers...
pause >nul

echo Stopping servers...
taskkill /FI "WindowTitle eq ReBook Backend*" /F >nul 2>&1
taskkill /FI "WindowTitle eq ReBook Frontend*" /F >nul 2>&1

echo Servers stopped.
pause
