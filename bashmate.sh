# Title: BashMate
# Language: Bourne Again Shell
# Creator: LounisBou
# Access: Public
# Category: System
# Type: Configuration
# Tags: bash, config, commands, tools
#
#
# Description: 
#
# Usage:
# Source this file in your .bashrc or .zshrc file.
#
#
# Get absolute directory of the current file.
currentDir="$(realpath $(dirname "$0"))"
# Check if .env file exists
if [ ! -f "$currentDir/.env" ]; then
  # Import .env file
  source "$currentDir/.env"
fi
#
# Import all files in the aliases directory.
for file in ${currentDir}/aliases/*; do source $file; done
# Enable nullglob to prevent errors if no matching files are found
shopt -s nullglob
# Check if there is at least one file with sh extension in the aliases private directory.
if compgen -G "${currentDir}/aliases_private/*.sh" > /dev/null; then
  # Import all files in the aliases private directory.
  for file in ${currentDir}/aliases_private/*.sh; do source $file; done
fi
# Disable nullglob 
shopt -u nullglob
# 
# Import all files in the functions directory.
for file in ${currentDir}/functions/*; do source $file; done
#
# ! DYNAMIC ALIASES
#
# Fonction to create dynamic alias. (dynamic alias are not saved in git)
function createAlias(){ 
  # Create alias for current session.
  alias "$*";
  # Create definitive alias.
  echo alias $* >> ${currentDir}/aliases_private/dynamic.sh
}