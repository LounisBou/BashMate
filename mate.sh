# Commands for BashMate
# Created by LounisBou

# Manage bashmate commands
# Usage: bashmate <command> <args>
function bashmate(){
    # Get first argument check if it's an existing function
    if declare -f "$1" > /dev/null
    then
        # Call function with arguments
        "$@"
    fi
}

# Show help
function help(){
    # Show help
    echo "BashMate commands:"
    echo "  bashmate <command> <args>"
    echo ""
    echo "Commands:"
    # List all commands
    list()
}

# Update bashmate
function update(){
    # Update bashmate
    cd ~/.bashmate && git pull
}

# Install bashmate
function install(){
    # Execute install script
    bash ~/.bashmate/installer.sh -i
}

# Uninstall bashmate
function uninstall(){
    # Execute install script
    bash ~/.bashmate/installer.sh -u
}

# List all commands
function list(){
    # List all commands
    echo "  bashmate help"
    echo "  bashmate update"
    echo "  bashmate install"
    echo "  bashmate uninstall"
    echo "  bashmate list"
    echo "  bashmate version"
    echo "  bashmate doctor"
    echo "  bashmate prune"
    echo "  bashmate reset"
    echo "  bashmate cleanup"
}

# Show version
function version(){
    # Show version
    echo "BashMate version: $(cat ~/.bashmate/version)"
    # Show bash version
    echo "Bash version: $BASH_VERSION"
}

# Doctor
function doctor(){
    # Check if brew is installed
    if ! command -v brew >/dev/null 2>&1; then
        echo "Brew is not installed. Please install it first."
        exit 1
    fi
    # Check if all brew packages from .Brewfile are installed
    brew bundle check --file=~/.Brewfile
}

