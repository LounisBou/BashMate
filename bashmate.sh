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
if [ -f "$currentDir/.env" ]; then
  # Import .env file
  source "$currentDir/.env"
fi
echo "ssh $KAP_PROD_SSH_USER@$KAP_PROD_URL -p $KAP_PROD_SSH_PORT"
#
# Import all files in the aliases directory.
for file in ${currentDir}/aliases/*; do source $file; done
# Create aliases personal file if not exists.
if [ ! -f "$currentDir/aliases_private/personal.sh" ]; then
  touch "$currentDir/aliases_private/personal.sh"
fi
# Import all files in the aliases private directory.
for file in ${currentDir}/aliases_private/*.sh; do source $file; done
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