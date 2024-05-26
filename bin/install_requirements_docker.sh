#!/bin/bash -e

echo "Compiling requirements..."
pip install pip-tools
pip-compile requirements-dashboard.in --resolver backtracking
echo "Installing requirements..."
pip install -r requirements-dashboard.txt
echo "Installation complete!";
