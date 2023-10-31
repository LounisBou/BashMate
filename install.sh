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
# Check if .zshrc exists
if [ -f "$HOME/.zshrc" ]; then
    # Check if BashMate is already installed in .zshrc
    if grep -q "bashmate.sh" "$HOME/.zshrc"; then
        echo "${YELLOW}BashMate is already installed in .zshrc${NC}"
        exit
    fi
    # Add BashMate sourcing to .zshrc
    echo "source $(PWD)/bashmate.sh" >> ~/.zshrc
    echo "${GREEN}BashMate installed in .zshrc${NC}"
    # Reload .zshrc
    source ~/.zshrc
fi

# Check if .bashrc exists
if [ -f "$HOME/.bashrc" ]; then
    # Check if BashMate is already installed in .bashrc
    if grep -q "bashmate.sh" "$HOME/.bashrc"; then
        echo "${YELLOW}BashMate is already installed in .bashrc${NC}"
        exit
    fi
    # Add BashMate sourcing to .bashrc
    echo "source $(PWD)/bashmate.sh" >> ~/.bashrc
    echo "${GREEN}BashMate installed in .bashrc${NC}"
    # Reload .bashrc
    source ~/.bashrc
fi

# Check if logo/logo.sh exists
if [ -f "logo/logo.sh" ]; then
    # Execute logo.sh
    ./logo/logo.sh
fi
echo ""

# Ask user if he wants to install BrewMate
read -p "Do you want to install BrewMate? (y/n) " -n 1 -r REPLY
echo ""

# Check if user wants to install BrewMate
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Execute brewmate.sh
    ./brewmate.sh
fi