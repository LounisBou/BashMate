#!/bin/bash

# Ask user if he wants to execute npm install
echo "--- NPM install ---"

# Ask user if he wants to execute npm install
read -p "Do you want to execute npm install? (y/n) " answer < /dev/tty

# Check the answer
if [ "$answer" == "y" ]; then
    # Execute npm install
    npm install
fi