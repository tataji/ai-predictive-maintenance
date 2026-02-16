#!/bin/bash

# AI Predictive Maintenance System - Installation Script
# This script sets up the complete system with all dependencies

set -e

echo "=========================================="
echo "AI Predictive Maintenance System"
echo "Installation Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
cd backend
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "To start the system:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "2. Open the frontend:"
echo "   Open frontend/index.html in your web browser"
echo "   OR serve it with: python -m http.server 8080 -d frontend"
echo ""
echo "3. Access the system:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend: http://localhost:8080 (if using http.server)"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "=========================================="
