#!/bin/bash
# Title: BashMate installer
# Creator: LounisBou
# Access: Public
# Category: System
# Type: Configuration
# Tags: bash, config, personal, installer
#
# Summary:
# Installer for BashMate.
#
# Usage:
# Execute install.sh file to install BashMate.
#
#
# Define colors for output.
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
# Define indent for output.
INDENT="    "
#
echo ""
#
# Check if .zshrc exists
if [ -f "$HOME/.zshrc" ]; then
    # Check if BashMate is already installed in .zshrc
    if grep -q "bashmate.sh" "$HOME/.zshrc"; then
        echo -e "${YELLOW}BashMate is already installed in .zshrc${NC}"
    else
        # Add BashMate sourcing to .zshrc
        echo "source $(PWD)/bashmate.sh" >> ~/.zshrc
        echo -e "${GREEN}BashMate installed in .zshrc${NC}"
        # Reload .zshrc
        source ~/.zshrc
    fi
fi

# Check if .bashrc exists
if [ -f "$HOME/.bashrc" ]; then
    # Check if BashMate is already installed in .bashrc
    if grep -q "bashmate.sh" "$HOME/.bashrc"; then
        echo -e "${YELLOW}BashMate is already installed in .bashrc${NC}"
    else
        # Add BashMate sourcing to .bashrc
        echo "source $(PWD)/bashmate.sh" >> ~/.bashrc
        echo -e "${GREEN}BashMate installed in .bashrc${NC}"
        # Reload .bashrc
        source ~/.bashrc
    fi
fi

# Check if logo/logo.sh exists
if [ -f "logo/logo.sh" ]; then
    # Execute logo.sh
    echo ""
    ./logo/logo.sh
    echo ""
fi
echo ""

# Ask user if he wants to install BrewMate
read -p "Do you want to install BrewMate? (y/n) " -n 1 -r REPLY

# Check if user wants to install BrewMate
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Execute brewmate.sh
    echo -e "\n"
    ./brewmate.sh -i
fi

# Message
echo -e "\n"
echo -e "${GREEN}BashMate installed.${NC}"
echo ""