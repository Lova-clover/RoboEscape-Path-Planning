#!/bin/bash

echo "========================================"
echo "RoboEscape: Algorithm Hunters"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/3] Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
fi

echo "[2/3] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo "[3/3] Starting game..."
echo ""
python main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Game crashed or exited with error"
    read -p "Press Enter to continue..."
fi

deactivate
