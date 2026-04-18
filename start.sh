#!/bin/bash
# Quick start script for NZ Address Checker
# This script helps you quickly start both frontend and backend

clear

echo "========================================"
echo "NZ Address Checker - Quick Start Guide"
echo "========================================"
echo ""
echo "This script will help you set up and run the application."
echo "Make sure you have:"
echo "  - Node.js 16+ and npm installed"
echo "  - Python 3.9+ installed"
echo "  - pip (Python package manager) installed"
echo ""

while true; do
    echo ""
    echo "Select an option:"
    echo "1. Install backend dependencies"
    echo "2. Install frontend dependencies"
    echo "3. Start backend (port 8000)"
    echo "4. Start frontend (port 5173)"
    echo "5. Run verification script"
    echo "6. Show API documentation"
    echo "7. Exit"
    echo ""
    
    read -p "Enter choice (1-7): " choice
    
    case $choice in
        1)
            echo ""
            echo "Installing backend dependencies..."
            cd backend
            pip install -r requirements.txt
            if [ $? -eq 0 ]; then
                echo ""
                echo "[OK] Backend dependencies installed successfully!"
                echo "Run: python -m uvicorn app.main:app --reload"
            else
                echo "[ERROR] Failed to install backend dependencies"
            fi
            cd ..
            ;;
        2)
            echo ""
            echo "Installing frontend dependencies..."
            cd frontend
            npm install
            if [ $? -eq 0 ]; then
                echo ""
                echo "[OK] Frontend dependencies installed successfully!"
                echo "Run: npm run dev"
            else
                echo "[ERROR] Failed to install frontend dependencies"
            fi
            cd ..
            ;;
        3)
            echo ""
            echo "Starting backend server on http://localhost:8000"
            echo "Press Ctrl+C to stop the server"
            echo ""
            cd backend
            python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
            cd ..
            ;;
        4)
            echo ""
            echo "Starting frontend dev server on http://localhost:5173"
            echo "Press Ctrl+C to stop the server"
            echo ""
            cd frontend
            npm run dev
            cd ..
            ;;
        5)
            echo ""
            echo "Running project verification..."
            python verify.py
            ;;
        6)
            echo ""
            echo "Available documentation:"
            echo "- README.md: Project overview and architecture"
            echo "- SETUP.md: Installation and running instructions"
            echo "- API.md: API endpoint documentation"
            echo "- COMPLETION_SUMMARY.md: Detailed completion report"
            echo ""
            echo "You can open these files with any text editor or browser."
            echo ""
            ;;
        7)
            echo ""
            echo "Thank you for using NZ Address Checker!"
            echo ""
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done
