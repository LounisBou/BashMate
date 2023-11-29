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
# Parameters:
# -h, --help: Show help.
# -i, --install: Install BrewMate.
# -u, --uninstall: Uninstall BrewMate.
#
# Define colors for output.
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
# Define indent for output.
INDENT="    "
#
# BrewMate path
BREWMATE_PATH="$(PWD)/BrewMate"
#
# Usage 
usage="Usage: install.sh [-h|--help] [-i|--install] [-u|--uninstall]"
#
# Check if parameter is given.
if [[ $# -eq 0 ]]; then
    echo -e "${RED}No parameter given.${NC}"
    echo -e "${YELLOW}$usage${NC}"
    exit
fi

# Get parameters, and check if they are valid.
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            echo "$usage"
            exit
        ;;
        -i|--install)
            install=true
            shift
        ;;
        -u|--uninstall)
            uninstall=true
            shift
        ;;
        *)
            echo -e "${RED}Invalid parameter: $key${NC}"
            echo -e "${YELLOW}$usage${NC}"
            exit
        ;;
    esac
done

# Check if install or uninstall parameter is given, but not both.
if [[ $install == true && $uninstall == true ]]; then
    echo -e "${RED}Invalid parameter, cannot install and uninstall at the same time.${NC}"
    echo -e "${YELLOW}$usage${NC}"
    exit
fi

# Check if install or uninstall parameter is given.
if [[ $install != true && $uninstall != true ]]; then
    echo -e "${RED}No parameter given.${NC}"
    echo -e "${YELLOW}$usage${NC}"
    exit
fi

echo -e "\n"

# Install BrewMate.
if [[ $install == true ]]; then

    # Check if .zshrc exists
    if [ -f "$HOME/.zshrc" ]; then
        # Check if BashMate is already installed in .zshrc
        if grep -q "bashmate.sh" "$HOME/.zshrc"; then
            echo -e "${YELLOW}BashMate is already installed in .zshrc${NC}"
        else
            # Check if Oh My Zsh is installed
            if [ -d "$HOME/.oh-my-zsh" ]; then
                # Ask user if he wants to install Oh My Zsh
                read -p "Do you want to install Oh My Zsh? (y/n) " -n 1 -r REPLY
                # Check if user wants to install Oh My Zsh
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    # Install Oh My Zsh
                    echo -e "\n"
                    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
                fi
            fi
            # Add BashMate sourcing to .zshrc
            echo "source $(PWD)/BashMate/bashmate.sh" >> ~/.zshrc
            echo -e "${GREEN}BashMate installed in .zshrc${NC}"
            # Inform user to reload .zshrc
            echo -e "${YELLOW}Please reload .zshrc to apply changes.${NC}"
            # Give user the command to reload .zshrc
            echo -e "${YELLOW}Command: source ~/.zshrc${NC}"
        fi
    fi

    # Check if .bashrc exists
    if [ -f "$HOME/.bashrc" ]; then
        # Check if BashMate is already installed in .bashrc
        if grep -q "bashmate.sh" "$HOME/.bashrc"; then
            echo -e "${YELLOW}BashMate is already installed in .bashrc${NC}"
        else
            # Add BashMate sourcing to .bashrc
            echo "source $(PWD)/BashMate/bashmate.sh" >> ~/.bashrc
            echo -e "${GREEN}BashMate installed in .bashrc${NC}"
            # Inform user to reload .bashrc
            echo -e "${YELLOW}Please reload .bashrc to apply changes.${NC}"
            # Give user the command to reload .bashrc
            echo -e "${YELLOW}Command: source ~/.bashrc${NC}"
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
        ${BREWMATE_PATH}/brewmate.sh -i
    fi

    # Message
    echo -e "\n ${GREEN}BashMate installed.${NC} \n"

# Uninstall BrewMate
elif [[ $uninstall == true ]]; then

    # Check if .zshrc exists
    if [ -f "$HOME/.zshrc" ]; then
        # Check if BashMate is already installed in .zshrc
        if grep -q "bashmate.sh" "$HOME/.zshrc"; then
            # Remove BashMate sourcing from .zshrc
            sed -i '' '/bashmate.sh/d' ~/.zshrc
            echo -e "${GREEN}BashMate uninstalled from .zshrc${NC}"
            # Reload .zshrc
            source ~/.zshrc
        else
            echo -e "${YELLOW}BashMate is not installed in .zshrc${NC}"
        fi
    fi

    # Check if .bashrc exists
    if [ -f "$HOME/.bashrc" ]; then
        # Check if BashMate is already installed in .bashrc
        if grep -q "bashmate.sh" "$HOME/.bashrc"; then
            # Remove BashMate sourcing from .bashrc
            sed -i '' '/bashmate.sh/d' ~/.bashrc
            echo -e "${GREEN}BashMate uninstalled from .bashrc${NC}"
            # Reload .bashrc
            source ~/.bashrc
        else
            echo -e "${YELLOW}BashMate is not installed in .bashrc${NC}"
        fi
    fi

    # Check if logo/logo.sh exists
    if [ -f "logo/logo.sh" ]; then
        # Execute logo.sh
        echo -e "\n"
        ./logo/logo.sh
        echo -e "\n"
    fi
    echo -e "\n"

    # Ask user if he wants to uninstall BrewMate
    read -p "Do you want to uninstall BrewMate? (y/n) " -n 1 -r REPLY

    # Check if user wants to uninstall BrewMate
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Execute brewmate.sh
        echo -e "\n"
        ${BREWMATE_PATH}/brewmate.sh -u
    fi

    # Message
    echo -e "\n ${GREEN}BashMate uninstalled.${NC} \n"

fi