@echo off
REM Quick start script for NZ Address Checker
REM This script helps you quickly start both frontend and backend

echo.
echo ========================================
echo NZ Address Checker - Quick Start Guide
echo ========================================
echo.

echo This script will help you set up and run the application.
echo Make sure you have:
echo   - Node.js 16+ and npm installed
echo   - Python 3.9+ installed
echo   - pip (Python package manager) installed
echo.

:menu
echo.
echo Select an option:
echo 1. Install backend dependencies
echo 2. Install frontend dependencies
echo 3. Start backend (port 8000)
echo 4. Start frontend (port 5173)
echo 5. Run verification script
echo 6. Show API documentation
echo 7. Exit
echo.

set /p choice="Enter choice (1-7): "

if "%choice%"=="1" goto install_backend
if "%choice%"=="2" goto install_frontend
if "%choice%"=="3" goto start_backend
if "%choice%"=="4" goto start_frontend
if "%choice%"=="5" goto verify
if "%choice%"=="6" goto docs
if "%choice%"=="7" goto end
echo Invalid choice. Please try again.
goto menu

:install_backend
echo.
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo.
    echo [OK] Backend dependencies installed successfully!
    echo Run: python -m uvicorn app.main:app --reload
) else (
    echo [ERROR] Failed to install backend dependencies
)
cd ..
goto menu

:install_frontend
echo.
echo Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% equ 0 (
    echo.
    echo [OK] Frontend dependencies installed successfully!
    echo Run: npm run dev
) else (
    echo [ERROR] Failed to install frontend dependencies
)
cd ..
goto menu

:start_backend
echo.
echo Starting backend server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
cd ..
goto menu

:start_frontend
echo.
echo Starting frontend dev server on http://localhost:5173
echo Press Ctrl+C to stop the server
echo.
cd frontend
call npm run dev
cd ..
goto menu

:verify
echo.
echo Running project verification...
python verify.py
goto menu

:docs
echo.
echo Opening documentation files...
echo.
echo Available documentation:
echo - README.md: Project overview and architecture
echo - SETUP.md: Installation and running instructions
echo - API.md: API endpoint documentation
echo - COMPLETION_SUMMARY.md: Detailed completion report
echo.
echo You can open these files with any text editor or browser.
echo.
goto menu

:end
echo.
echo Thank you for using NZ Address Checker!
echo.
