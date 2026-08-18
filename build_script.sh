#!/bin/bash
set -e

echo "Installing dependencies with pip (bypassing uv)..."
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install --no-cache-dir psycopg[binary]==3.1.19
python3 -m pip install --no-cache-dir Flask==3.0.0
python3 -m pip install --no-cache-dir flask-cors==4.0.0
python3 -m pip install --no-cache-dir python-dotenv==1.0.0
python3 -m pip install --no-cache-dir Werkzeug==3.0.0

echo "Build complete!"
