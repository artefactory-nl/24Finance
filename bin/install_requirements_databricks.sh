#!/bin/bash -e

echo "Compiling requirements..."
pip install pip-tools
pip-compile ../requirements.in --resolver backtracking
echo "Installing requirements..."
pip install -r ../requirements.txt
echo "Installation complete!";
