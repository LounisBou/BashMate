# Aliases for directories management
# Created by LounisBou

# GLOBAL VARIABLES

# COMMANDS

# Create a new directory and move to it
function dir-mk() {
    mkdir -p "$1" && cd "$1"
}

# Recursively remove a directory
function dir-rm() {
    rm -rf "$1"
}

# Change to a directory and list its content
function dir-cd() {
    cd "$1" && ll
}

# List directories
function dir-ls() {
    ls -da */
}

# List directories with details
function dir-ll() {
    ls -lda */
}
