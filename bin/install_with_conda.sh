#!/bin/bash -e

read -p "Want to install conda env named '24Finance'? (y/n)" answer
if [ "$answer" = "y" ]; then
  echo "Installing conda env..."
  conda create -n 24Finance python=3.10 -y
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate 24Finance
  echo "Compiling requirements..."
  pip install pip-tools
  pip-compile requirements-developer.in --resolver backtracking
  pip-compile requirements.in --resolver backtracking
  echo "Installing requirements..."
  pip install -r requirements-developer.txt
  python3 -m ipykernel install --user --name=24Finance
  conda install -c conda-forge --name 24Finance notebook -y
  # echo "Installing pre-commit..."
  # make install_precommit
  echo "Installation complete!";
else
  echo "Installation of conda env aborted!";
fi
