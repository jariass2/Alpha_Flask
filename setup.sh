#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install flask flask-login

# Print success message
echo "Setup complete! Your virtual environment is ready."
echo "To run the Flask app, make sure to activate the virtual environment first:"
echo "source venv/bin/activate"
echo "Then run: python app.py"
