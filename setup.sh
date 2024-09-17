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

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install PyTorch separately with the correct URL
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 -f https://download.pytorch.org/whl/torch_stable.html

# Install the remaining dependencies
pip install -r requirements.txt

# Inform the user
echo "Environment setup complete."

# Keep the environment active
exec bash --rcfile <(echo "source venv/bin/activate")
