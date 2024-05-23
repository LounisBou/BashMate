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

# Open a new tab in iTerm2, with the current directory and execute a command if provided
function tab() {
    # Check if command is not empty
    if [ -n "$*" ]; then
        # Retrieve command
        command="$*"
    fi
    osascript -e "tell application \"iTerm2\"" \
                -e "tell current window" \
                -e "create tab with default profile" \
                -e "tell current session" \
                -e "write text \"cd \" & quoted form of (do shell script \"pwd\") & \"; clear; $command\"" \
                -e "end tell" \
                -e "end tell" \
                -e "end tell"
}
# Bind CTRL+T to open a new tab in iTerm2
bindkey '^T' tab

# Open a new window in iTerm2, with the current directory and execute a command if provided
function win() {
    # Check if command is not empty
    if [ -n "$*" ]; then
        # Retrieve command
        command="$*"
    fi
    osascript -e "tell application \"iTerm2\"" \
                -e "create window with default profile" \
                -e "tell current session of current window" \
                -e "write text \"cd \" & quoted form of (do shell script \"pwd\") & \"; clear; $command\"" \
                -e "end tell" \
                -e "end tell"
}
# Bind CTRL+W to open a new window in iTerm2
bindkey '^W' win