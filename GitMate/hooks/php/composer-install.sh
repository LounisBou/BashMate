#!/bin/bash

# Ask user if he wants to execute composer install
echo "--- Composer install ---"

# Ask user if he wants to execute composer install
read -p "Do you want to execute composer install? (y/n) " answer < /dev/tty

# Check the answer
if [ "$answer" == "y" ]; then
    # Execute composer install
    composer install
fi