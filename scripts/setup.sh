#!/bin/bash
# Setup script for development environment

echo "🔧 Setting up Strategy Project..."

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "✅ Setup complete! Run 'source .venv/bin/activate' to activate the environment"
