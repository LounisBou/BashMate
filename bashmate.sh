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
# Import .env file
source "$currentDir/.env"
#
# Import all files in the aliases directory.
for file in ${currentDir}/aliases/*; do source $file; done
# Check if there is at least one file in the aliases private directory.
if [ "$(ls -A ${currentDir}/aliases_private)" ]; then
  # Import all files in the aliases private directory.
  for file in ${currentDir}/aliases_private/*.sh; do source $file; done
fi
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