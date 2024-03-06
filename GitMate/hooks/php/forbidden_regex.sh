#!/bin/bash

# Check for forbidden regex patterns in the files being committed
# Use forbidden_regex.txt to define the patterns
echo "--- Forbidden Regex ---"

# Define file extensions separate by space. If empty, apply to all files.
file_extensions="php"

# Flag to track if any error was found
error_found=0

# Get the list of files that are being committed (available in the pre-commit hook via the files variable)
# files=$(git diff --cached --name-only --diff-filter=ACM "$against")

# Filter the files list based on the file extensions
if [ -n "$file_extensions" ]; then
    files_to_check=$(echo "$files" | grep -E ".*\.($file_extensions)$")
else
    files_to_check=$files
fi

# Initialize the array
regex=()

# Read regex patterns from an external file into an array
# SCRIPT_DIR is defined in the pre-commit hook
while IFS= read -r line; do
    regex+=("$line")
done < "$SCRIPT_DIR/php/forbidden_regex.txt"

# Iterate through the files_to_check
for file in $files_to_check
do
    # Iterate through the regex patterns and check if the file contains any of the patterns
    for pattern in "${regex[@]}"
    do
       # Use grep with -n for line numbers. Capture output if there's a match.
       matches=$(grep -n -E "$pattern" "$file")
       if [ ! -z "$matches" ]; then
           # Set the flag to indicate an error was found
           error_found=1
           # Print each matching line and its line number
           while IFS= read -r line; do
               echo "Error: The file $file contains the forbidden pattern: $line"
           done <<< "$matches"
       fi
    done
done

# After all files and patterns have been checked, decide what to do if any error was found
if [ "$error_found" -eq 1 ]; then
    echo "Forbidden patterns were found in one or more files."
    exit 1
fi
