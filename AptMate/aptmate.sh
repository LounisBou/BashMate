# Title: AptMate install script
# Creator: LounisBou
# Access: Public
# Category: System
# Type: Configuration
# Tags: apt, aptitude, config, personal
#
# Summary:
# Configuration files for debian based distribution (apache, php, mysql, etc.).
#
# Usage:
# Execute aptmate.sh file to launch installation.
#
# Usage 
usage="Usage: aptmate.sh"
# Get absolute directory of the current file.
currentDir="$(realpath $(dirname "$0"))"
# Define colors for output.
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Define indent for output.
INDENT="    "

# List of packages to install.
packages=(
    "git"
    "wget"
    "curl"
    "htop"
    "nmap"
    "vim"
)