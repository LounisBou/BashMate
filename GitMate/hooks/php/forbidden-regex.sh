#!/bin/bash

# Define file extensions separate by space. If empty, apply to all files.
file_extensions="php"

# Flag to track if any error was found
error_found=0

# Filter the files list based on the file extensions
if [ -n "$file_extensions" ]; then
    files=$(echo "$files" | grep -E ".*\.($file_extensions)$")
fi

# Initialize the array
regex=()

# Read regex patterns from an external file into an array
while IFS= read -r line; do
    regex+=("$line")
done < "$SCRIPT_DIR/php/forbidden-regex.txt"

# Iterate through the files
for file in $files
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

# If the script reaches here, it means the commit is allowed
exit 0