#!/bin/bash
# iTerm Aliases
# Created by Lounis Bouchentouf

# Open iTerm tab with a specific tab name and directory
function iterm-tab(){
    # Get first argument as tab name
    tab_name=$1
    # Get second argument as working path
    working_path=$2
    # Open iTerm tab with tab name and working path
    osascript -e "tell application \"iTerm\" to tell current window to set newTab to (create tab with default profile)"
    osascript -e "tell application \"iTerm\" to tell current session of current window to write text \"cd $working_path\""
    osascript -e "tell application \"iTerm\" to tell current session of current window to write text \"clear\""
    osascript -e "tell application \"iTerm\" to tell current session of current window to write text \"echo -n -e \"\\033]0;$tab_name\\007\"\""
}