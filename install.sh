#!/bin/bash

# Find the Python script's directory
pythonDir=$(dirname $(which python))

# Add the Python scripts directory to PATH if it's not already included
echo "Checking if PATH needs to be updated..."
if [[ ":$PATH:" != *":$pythonDir:"* ]]; then
    echo "Updating PATH to include Python scripts"
    export PATH="$PATH:$pythonDir"
    echo 'export PATH="$PATH:'$pythonDir'"' >>~/.bashrc
fi

# Install your Python package
(cd "$(dirname "$0")" && pip install .)

echo "Installation complete. Please restart your terminal or start a new one for the PATH changes to take effect."
