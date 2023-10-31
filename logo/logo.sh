#!/bin/bash

# Get absolute directory of the current file.
currentDir="$(realpath $(dirname "$0"))"

# Define color reset
NC='\033[0m'

# Define colors
green='\033[0;32m'

# Show BashMate logo
logo=$(cat $currentDir/logo-ascii.txt)

# Show logo
echo -e "${green}$logo${NC}"
