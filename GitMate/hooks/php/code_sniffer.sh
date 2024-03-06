#!/bin/bash

echo "--- Code Sniffer ---"

# Define file extensions separate by space. If empty, apply to all files.
file_extensions="php"

# Counter to track how many errors were found
errors_found=0

# Check if CodeSniffer is installed
if ! command -v phpcs &> /dev/null
then
    # Install CodeSniffer
    echo "CodeSniffer is not installed. Attempting to install it..."
    composer global require "squizlabs/php_codesniffer=*"
    # Check if the composer bin dir is in the PATH
    if [[ ":$PATH:" != *":$HOME/.composer/vendor/bin:"* ]]; then
        # Print the instructions to add the composer bin dir to the PATH
        echo "The composer bin directory is not in the PATH. Add the following line to your .bashrc, .zshrc or .bash_profile and restart your terminal:"
        echo "export PATH=\"$HOME/.composer/vendor/bin:\$PATH\""
    fi
fi

# Get the list of files that are being committed (available in the pre-commit hook via the files variable)
# files=$(git diff --cached --name-only --diff-filter=ACM "$against")

# Filter the files list based on the file extensions
if [ -n "$file_extensions" ]; then
    files_to_check=$(echo "$files" | grep -E ".*\.($file_extensions)$")
else
    files_to_check=$files
fi

# Iterate through the files_to_check
for file in $files_to_check
do
    # Run CodeSniffer on the file
    errors=$(phpcs --standard=PSR2 "$file")
    if [ ! -z "$errors" ]; then
        # Increment the counter to indicate an error was found
        errors_found=$((errors_found+1))
        # Print the error
        echo "Error: The file $file contains the following CodeSniffer errors:"
        echo "$errors"
    fi
done

# After all files have been checked, decide what to do if any error was found
if [ "$errors_found" -gt 0 ]; then
    # Print the error message
    echo "CodeSniffer errors were found in one or more files."
    # Use read command with -p option for prompt and < /dev/tty to explicitly read from the terminal
    read -p "Do you want to fix the errors automatically? (y/n) " answer < /dev/tty
    # Check the answer
    if [ "$answer" == "y" ]; then
        # Fix the errors automatically
        phpcbf --standard=PSR2 $files_to_check
        echo "CodeSniffer errors were fixed."
    else
        # Ask the user to fix the errors manually
        echo "Please fix the errors manually and try again."
        # Or run commit again, with the --no-verify option to skip the pre-commit hook
        echo "You can also run the commit again, with the --no-verify option to skip the pre-commit hook."
        echo "git commit --no-verify"
        # Exit with an error
        exit 1
    fi
fi
