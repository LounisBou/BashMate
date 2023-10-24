#!/bin/bash

# Define color reset
NC='\033[0m'

# Define colors
green='\033[0;32m'

# Show BashMate logo
logo=$(cat logo-ascii.txt)

# Show logo
echo -e "${green}$logo${NC}"