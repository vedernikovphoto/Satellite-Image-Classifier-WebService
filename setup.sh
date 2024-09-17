#!/bin/bash

# Update package list and install system dependencies
# sudo apt-get update
# sudo apt-get install -y libgl1-mesa-glx

# Install NVIDIA Container Toolkit (Host setup)
# sudo apt-key adv --fetch-keys https://nvidia.github.io/nvidia-docker/gpgkey
# distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
# curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
# sudo apt-get update
# sudo apt-get install -y nvidia-container-toolkit
# sudo systemctl restart docker

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
