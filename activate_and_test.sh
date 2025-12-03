#!/bin/bash
# Quick activation and test script

echo "=========================================="
echo "Flow Control System - Activation Script"
echo "=========================================="
echo ""

# Activate virtual environment
echo "1. Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "2. Installing dependencies..."
    pip install -r requirements.txt
else
    echo "2. Dependencies already installed ✓"
fi

echo ""
echo "3. Testing the system..."
python example_usage.py

echo ""
echo "=========================================="
echo "Setup complete! Your virtual environment is active."
echo ""
echo "Next steps:"
echo "  - Use in code: from flow_control.login_hook import resolve_login_redirect"
echo "  - Start API: uvicorn api.main:app --reload"
echo "  - Deactivate: deactivate"
echo "=========================================="

