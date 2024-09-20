#!/bin/bash

# Check if Python 3.9 is installed
if ! python3.9 --version &>/dev/null; then
    echo "Python 3.9 is required but not installed. Please install Python 3.9."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3.9 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
pip install -r requirements.txt

echo "Environment setup complete."
exec bash --rcfile <(echo "source venv/bin/activate")
