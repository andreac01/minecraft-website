#!/bin/bash

# Get the model
if [ -f "Qwen2.5-0.5B-Instruct-IQ4_XS.gguf" ]; then
	echo "Model found."
else
	echo "Model not found. Downloading..."
	wget https://huggingface.co/bartowski/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-IQ4_XS.gguf

# Create a virtual environment named 'website_venv'
if [ -d "website_venv" ]; then
	echo "Virtual environment found."
else
	echo "Virtual environment not found. Creating..."
	python3 -m venv website_venv
	echo "Virtual environment 'website_venv' created."

# Activate the virtual environment
source website_venv/bin/activate

# Install the required packages
echo "Installing the required packages..."
pip install -r requirements.txt

# Run the application
echo "Running the application..."
nohup python app.py & > /dev/null 2>&1
echo "Ready"

# Deactivate the virtual environment
deactivate
