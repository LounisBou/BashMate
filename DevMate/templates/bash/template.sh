#!/usr/bin/env bash
# Title: 
# Language: Bourne Again Shell
# Creator: LounisBou
# Access: Public
#
# Summary:
# 
#
# Description: 
#
# 
# Parameters:
# -h, --help: Show help.
# -i, --install: Install
# -u, --uninstall: Uninstall
#
# Usage:
# 
usage="Usage: example.sh [-h|--help] [-i|--install] [-u|--uninstall]"
#
#
# Define colors for output.
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
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