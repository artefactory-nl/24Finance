#!/bin/bash -e

read -p "Want to install conda env named 'artefact-hackathon-team-04'? (y/n)" answer
if [ "$answer" = "y" ]; then
  echo "Installing conda env..."
  conda create -n artefact-hackathon-team-04 python=3.10 -y
  source $(conda info --base)/etc/profile.d/conda.sh
  conda activate artefact-hackathon-team-04
  echo "Installing requirements..."
  pip install -r requirements-developer.txt
  python3 -m ipykernel install --user --name=artefact-hackathon-team-04
  conda install -c conda-forge --name artefact-hackathon-team-04 notebook -y
  # echo "Installing pre-commit..."
  # make install_precommit
  echo "Installation complete!";
else
  echo "Installation of conda env aborted!";
fi
