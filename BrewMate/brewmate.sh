# Title: BrewMate install script
# Creator: LounisBou
# Access: Public
# Category: System
# Type: Configuration
# Tags: brew, config, personal
#
# Summary:
# Configuration files for brew (apache, php, mysql, etc.).
#
# Usage:
# Execute brewmate.sh file to override your brew configuration by BrewMate one.
# Parameters:
# -h, --help: Show help.
# -i, --install: Install BrewMate.
# -u, --uninstall: Uninstall BrewMate.
#
# Usage 
usage="Usage: brewmate.sh [-h|--help] [-i|--install] [-u|--uninstall]"
# Get absolute directory of the current file.
currentDir="$(realpath $(dirname "$0"))"
# System homebrew etc directory.
systemHomebrewEtcDir="/opt/homebrew/etc"
# BrewMate homebrew etc directory.
brewMateHomebrewEtcDir="${currentDir}/opt/homebrew/etc"
# Define colors for output.
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Define indent for output.
INDENT="    "

# Check if brew is installed.
if ! command -v brew &> /dev/null; then
    echo "${RED}Brew is not installed.${NC}"
    echo "Install brew first, using this command:"
    echo "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit
fi

# Check if parameter is given.
if [[ $# -eq 0 ]]; then
    echo "${RED}No parameter given.${NC}"
    echo "${YELLOW}$usage${NC}"
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
            echo "${RED}Invalid parameter.${NC}"
            echo "${YELLOW}$usage${NC}"
            exit
        ;;
    esac
done

# Check if install or uninstall parameter is given, but not both.
if [[ $install == true && $uninstall == true ]]; then
    echo "${RED}Invalid parameter, cannot install and uninstall at the same time.${NC}"
    echo "${YELLOW}$usage${NC}"
    exit
fi

# Check if install or uninstall parameter is given.
if [[ $install != true && $uninstall != true ]]; then
    echo "${RED}No parameter given.${NC}"
    echo "${YELLOW}$usage${NC}"
    exit
fi

# Install BrewMate.
if [[ $install == true ]]; then

    # Check if brewmate is already installed. 
    # By checking if brewmate.conf symlink exists in /opt/homebrew/etc.
    if [[ -L "$systemHomebrewEtcDir/brewmate.conf" ]]; then
        echo "${GREEN}BrewMate is already installed.${NC}"
        echo "${GREEN}Nothing to do.${NC}"
        exit
    fi

    # Message.
    echo "${GREEN}Installing BrewMate...${NC}"
    
    # Ask user if he wants to update brew.
    read -p "Do you want to update brew? It's recommended to do it before installing BrewMate. (y/n) " -n 1 -r REPLY
    echo ""
    # Check if user wants to update brew.
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Update brew.
        brew update
    fi
    

    # Ask user if he wants to install brew packages from Brewfile.
    read -p "Do you want to install brew packages from Brewfile? (y/n) " -n 1 -r REPLY
    echo ""
    # Check if user wants to install brew packages from Brewfile.
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Install brew packages from Brewfile.
        brew bundle install ${currentDir}/.Brewfile
    fi

    # Ask user if he wants to upgrade brew packages.
    read -p "Do you want to upgrade brew packages? (y/n) " -n 1 -r REPLY
    echo ""
    # Check if user wants to upgrade brew packages.
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Upgrade brew packages.
        brew upgrade
    fi

    # Create symbolic link for each folders and files entries in ./opt/homebrew/etc in /opt/homebrew/etc.
    for entry in ${brewMateHomebrewEtcDir}/*; do 
        # Backup : If entry already exists in /opt/homebrew/etc.
        if [[ -e ${systemHomebrewEtcDir}/$(basename $entry) ]]; then
            # Echo message for entry backup.
            echo "${INDENT}${YELLOW}$(basename $entry) exists in target${NC}"
            echo "${INDENT}${GREEN}Backup $(basename $entry)${NC}"
            # Create backup of entry.
            mv ${systemHomebrewEtcDir}/$(basename $entry) ${systemHomebrewEtcDir}/$(basename $entry).bak
        fi
        # Echo message for entry installation.
        echo "${INDENT}Installing $(basename $entry) in $systemHomebrewEtcDir"
        # Create symbolic link not already existing.
        ln -s $entry $systemHomebrewEtcDir;
    done

    # Message.
    echo "${GREEN}BrewMate installed.${NC}"

# Uninstall brewmate
elif [[ $uninstall == true ]]; then

    # Check if brewmate is already uninstalled. 
    # By checking if /opt/homebrew/etc/brewmate.conf exists.
    if [[ ! -f "$systemHomebrewEtcDir/brewmate.conf" ]]; then
        echo "${YELLOW}BrewMate is not installed.${NC}"
        echo "${YELLOW}Nothing to do.${NC}"
        exit
    fi

    # Message.
    echo "${GREEN}Uninstalling BrewMate...${NC}"

    # Remove symbolic link for each folders and files entries in ./opt/homebrew/etc in /opt/homebrew/etc.
    for entry in ${brewMateHomebrewEtcDir}/*; do 
        # Check if entry is a symbolic link.
        if [[ -L ${systemHomebrewEtcDir}/$(basename $entry) ]]; then
            # Echo message for entry uninstallation.
            echo "${INDENT}${YELLOW}Uninstalling $(basename $entry)"
            # Remove symbolic link.
            rm ${systemHomebrewEtcDir}/$(basename $entry); 
            # Restore : If backup of entry exists in /opt/homebrew/etc.
            if [[ -e ${systemHomebrewEtcDir}/$(basename $entry).bak ]]; then
                # Echo message for entry restore.
                echo "${INDENT}${GREEN}Restoring backup of $(basename $entry)${NC}"
                # Restore entry.
                mv ${systemHomebrewEtcDir}/$(basename $entry).bak ${systemHomebrewEtcDir}/$(basename $entry)
            fi
        else
            echo "${INDENT}$(basename $entry) is not a symbolic link, skipping."
        fi
    done

    # Dump brew packages.
    brew bundle dump --force --file=${currentDir}/.Brewfile
    
    # Ask user if he wants to uninstall brew packages.
    read -p "Do you want to uninstall brew packages? (y/n) " -n 1 -r REPLY
    echo "\n"

    # Check if user wants to uninstall brew packages.
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Warning message.
        echo "${RED}Be careful, this will uninstall all packages installed with BrewMate.${NC}"
        # Confirm message.
        read -p "${RED}ARE YOU SURE? (y/n)${NC} " -n 1 -r REPLY
        # Check if user wants to uninstall brew packages.
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Uninstall brew packages.
            brew bundle cleanup --force --file=${currentDir}/.Brewfile
            # Message.
            echo "${GREEN}Brew packages uninstalled.${NC}"
            echo "\n"
        fi
    fi

    # Show message.
    echo "${GREEN}BrewMate uninstalled.${NC}"

fi