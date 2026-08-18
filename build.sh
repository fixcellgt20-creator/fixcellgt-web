#!/bin/bash
set -e

echo "Installing dependencies with pip (not uv)..."
python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r requirements.txt

echo "Build complete!"
