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
# Check if brew is installed.
if ! command -v brew &> /dev/null
then
    echo "Brew is not installed."
    echo "Install brew first, using this command:"
    echo "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit
fi

# Check if parameter is given.
if [[ $# -eq 0 ]]
then
    echo "No parameter given."
    echo "$usage"
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
            echo "Invalid parameter."
            echo "$usage"
            exit
        ;;
    esac
done

# Check if install or uninstall parameter is given, but not both.
if [[ $install == true && $uninstall == true ]]
then
    echo "Invalid parameter, cannot install and uninstall at the same time."
    echo "$usage"
    exit
fi

# Check if install or uninstall parameter is given.
if [[ $install != true && $uninstall != true ]]
then
    echo "No parameter given."
    echo "$usage"
    exit
fi



# Install BrewMate.
if [[ $install == true ]]
then
    # Check if brewmate is already installed. 
    # By checking if /opt/homebrew/etc/brewmate.conf exists.
    if [[ -f "/opt/homebrew/etc/brewmate.conf" ]]
    then
        echo "BrewMate is already installed."
        exit
    fi

    # Create symbolic link for each folders and files entries in ./opt/brew/homebrew/etc in /opt/homebrew/etc.
    for entry in ${currentDir}/brew/opt/homebrew/etc/*; 
    do 
        # Echo message for entry installation.
        echo "Installing $entry"
        # Check if entry is a directory.
        if [[ -d /opt/homebrew/etc/$(basename $entry) ]]
        then
            echo "$entry is a directory, skipping."
            continue
        else
            # Echo message for entry installation.
            echo "Installing $entry"
        fi
        # Create symbolic link.
        # -s: Create a symbolic link.
        # -f: If the target file already exists, then unlink it so that the link may occur.
        # -n: If the target_file or target_dir is a symbolic link, do not follow it.  This is most useful with the -f option, to replace a symlink which may point to a directory.
        ln -s $entry /opt/homebrew/etc;
    done
    # Show message.
    echo "BrewMate installed."

# Uninstall brewmate
elif [[ $uninstall == true ]]
then
    # Check if brewmate is already uninstalled. 
    # By checking if /opt/homebrew/etc/brewmate.conf exists.
    if [[ ! -f "/opt/homebrew/etc/brewmate.conf" ]]
    then
        echo "BrewMate is not installed."
        echo "Nothing to do."
        exit
    fi

    # Remove symbolic link for each folders and files entries in ./opt/brew/homebrew/etc in /opt/homebrew/etc.
    for entry in ${currentDir}/brew/opt/homebrew/etc/*;  
    do 
        # Check if entry is a symbolic link.
        if [[ -L /opt/homebrew/etc/$(basename $entry) ]]
        then
            # Echo message for entry uninstallation.
            echo "Uninstalling $entry"
            # Remove symbolic link.
            rm /opt/homebrew/etc/$(basename $entry); 
        else
            echo "$entry is not a symbolic link, skipping."
        fi
    done
    # Show message.
    echo "BrewMate uninstalled."
fi