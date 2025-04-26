#!/bin/bash

# ASCII art banner
echo "======================================"
echo "  Arabic PDF Generator Setup Script"
echo "======================================"

# Create logs directory if it doesn't exist
mkdir -p logs

# Create static/pdfs directory if it doesn't exist
mkdir -p app/static/pdfs

# Install dependencies
echo "Installing dependencies..."
poetry install

# Run the application
echo "Starting the application..."
export FLASK_APP=app
export FLASK_ENV=development
poetry run flask run --host=0.0.0.0