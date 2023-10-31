# Title: Brew config
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
brewMateHomebrewEtcDir="${currentDir}/brew/opt/homebrew/etc"

# Define colors for output.
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Define indent for output.
INDENT="    "

# Check if brew is installed.
if ! command -v brew &> /dev/null
then
    echo "${RED}Brew is not installed.${NC}"
    echo "Install brew first, using this command:"
    echo "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit
fi

# Check if parameter is given.
if [[ $# -eq 0 ]]
then
    echo "${RED}No parameter given.${NC}"
    echo "${YELLOW}$usage${NC}"
    exit
fi

# Get parameters, and check if they are valid.
while [[ $# -gt 0 ]]
do
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
if [[ $install == true && $uninstall == true ]]
then
    echo "${RED}Invalid parameter, cannot install and uninstall at the same time.${NC}"
    echo "${YELLOW}$usage${NC}"
    exit
fi

# Check if install or uninstall parameter is given.
if [[ $install != true && $uninstall != true ]]
then
    echo "${RED}No parameter given.${NC}"
    echo "${YELLOW}$usage${NC}"
    exit
fi



# Install BrewMate.
if [[ $install == true ]]
then
    # Check if brewmate is already installed. 
    # By checking if brewmate.conf exists in target directory.
    if [[ -f "$systemHomebrewEtcDir/brewmate.conf" ]]
    then
        echo "${GREEN}BrewMate is already installed.${NC}"
        echo "${GREEN}Nothing to do.${NC}"
        exit
    fi

    # Message.
    echo "${GREEN}Installing BrewMate...${NC}"

    # Create symbolic link for each folders and files entries in ./opt/brew/homebrew/etc in /opt/homebrew/etc.
    for entry in ${brewMateHomebrewEtcDir}/*; 
    do 
        # Backup : If entry already exists in /opt/homebrew/etc.
        if [[ -e ${systemHomebrewEtcDir}/$(basename $entry) ]]
        then
            # Echo message for entry backup.
            echo "${INDENT}${YELLOW}$(basename $entry) exists in target${NC}"
            echo "${INDENT}${GREEN}Backup $(basename $entry)${NC}"
            # Create backup of entry.
            mv ${systemHomebrewEtcDir}/$(basename $entry) ${systemHomebrewEtcDir}/$(basename $entry).bak
        fi
        # Echo message for entry installation.
        echo "${INDENT}Installing $(basename $entry) in $systemHomebrewEtcDir"
        # Create symbolic link.
        ln -s $entry $systemHomebrewEtcDir;
    done
    # Show message.
    echo "${GREEN}BrewMate installed.${NC}"

# Uninstall brewmate
elif [[ $uninstall == true ]]
then
    # Check if brewmate is already uninstalled. 
    # By checking if /opt/homebrew/etc/brewmate.conf exists.
    if [[ ! -f "$systemHomebrewEtcDir/brewmate.conf" ]]
    then
        echo "${YELLOW}BrewMate is not installed.${NC}"
        echo "${YELLOW}Nothing to do.${NC}"
        exit
    fi

    # Message.
    echo "${GREEN}Uninstalling BrewMate...${NC}"

    # Remove symbolic link for each folders and files entries in ./opt/brew/homebrew/etc in /opt/homebrew/etc.
    for entry in ${brewMateHomebrewEtcDir}/*;  
    do 
        # Check if entry is a symbolic link.
        if [[ -L ${systemHomebrewEtcDir}/$(basename $entry) ]]
        then
            # Echo message for entry uninstallation.
            echo "${INDENT}${YELLOW}Uninstalling $(basename $entry)"
            # Remove symbolic link.
            rm ${systemHomebrewEtcDir}/$(basename $entry); 
            # Restore : If backup of entry exists in /opt/homebrew/etc.
            if [[ -e ${systemHomebrewEtcDir}/$(basename $entry).bak ]]
            then
                # Echo message for entry restore.
                echo "${INDENT}${GREEN}Restoring backup of $(basename $entry)${NC}"
                # Restore entry.
                mv ${systemHomebrewEtcDir}/$(basename $entry).bak ${systemHomebrewEtcDir}/$(basename $entry)
            fi
        else
            echo "${INDENT}$(basename $entry) is not a symbolic link, skipping."
        fi
    done
    # Show message.
    echo "${GREEN}BrewMate uninstalled.${NC}"
fi