#!/bin/bash
# Quick start script for the hidden admin page

echo "=========================================="
echo "🔒 Starting Flow Control Admin Server"
echo "=========================================="
echo ""

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "1. Activating virtual environment..."
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv .venv"
    exit 1
fi

# Install dependencies if needed
echo "2. Checking dependencies..."
if ! python -c "import fastapi" 2>/dev/null || ! python -c "import multipart" 2>/dev/null; then
    echo "   Installing dependencies..."
    pip install -r requirements.txt -q
fi

echo ""
echo "=========================================="
echo "✅ Server Starting..."
echo "=========================================="
echo ""
echo "🔒 Admin Page URL:"
echo "   http://localhost:8000/admin-flow-control-secret-2024"
echo ""
echo "🔐 Login Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

