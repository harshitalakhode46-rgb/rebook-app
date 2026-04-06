#!/bin/bash
# ReBook Application Startup Script for Mac/Linux
# This script starts both backend and frontend servers

echo "========================================"
echo "Starting ReBook Application"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run setup first:"
    echo "  cd backend"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  python setup.py"
    exit 1
fi

# Check if database exists
if [ ! -f "backend/rebook.db" ]; then
    echo "Warning: Database not found!"
    echo "Running setup script..."
    cd backend
    source venv/bin/activate
    python setup.py
    cd ..
fi

echo "Starting Backend Server..."
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting Frontend Server..."
cd frontend
python3 -m http.server 8080 &
FRONTEND_PID=$!
cd ..

echo
echo "========================================"
echo "ReBook is now running!"
echo "========================================"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:8080"
echo
echo "Press Ctrl+C to stop all servers..."

# Wait for Ctrl+C
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
