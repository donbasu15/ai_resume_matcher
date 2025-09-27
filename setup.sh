#!/bin/bash

# AI Resume Matcher Setup Script
echo "🚀 Setting up AI Resume Matcher..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python packages..."
pip install -r requirements.txt

# Download spaCy model
echo "🔽 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p logs
mkdir -p data/models

# Set permissions
chmod 755 uploads
chmod 755 logs

echo "✅ Setup complete!"
echo ""
echo "🎉 To start the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python app/main.py"
echo "3. Open your browser and go to: http://localhost:5000"
echo ""
echo "📖 For more information, see README.md"