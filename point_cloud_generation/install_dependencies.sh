#!/bin/bash

# Ensure the script exits on any error
set -e

# Update package list and install pip if not already installed
if ! command -v pip &> /dev/null; then
    echo "pip not found, installing..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Install the required Python packages
pip install numpy opencv-python tqdm open3d transformers Pillow requests ffmpeg-python

echo "All dependencies have been installed successfully."
