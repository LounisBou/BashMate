#!/bin/bash

# Check if some commit message contains "WIP"
echo "--- WIP Commit ---"

# Get all commit messages in the range of commits to examine (available in the pre-push hook via the commit_messages variable)
#commit_messages=$(git log --format=%s "$range")

# Counter to track how many errors were found
errors_found=0

# Initialize the array of forbidden messages
forbidden_messages=()

# Read forbidden messages from an external file into an array
# SCRIPT_DIR is defined in the pre-push hook
while IFS= read -r line; do
    forbidden_messages+=("$line")
done < "$SCRIPT_DIR/git/forbidden_commit.txt"

# Loop through all commit messages
for message in $commit_messages
do
    # Put the message in lowercase
    message_lowercase=$(echo "$message" | tr '[:upper:]' '[:lower:]')
    # Check if the commit message contains one of the forbidden messages
    for forbidden_message in "${forbidden_messages[@]}"
    do
        # Use grep with -n for line numbers. Capture output if there's a match.
        matches=$(echo "$message_lowercase" | grep -n -E "$forbidden_message")
        if [ ! -z "$matches" ]; then
            # Increment the counter to indicate an error was found
            errors_found=$((errors_found+1))
            # Print the matching commit message
            echo "Error: The commit message \"$message\" contains the forbidden message : $forbidden_message"
        fi
    done
done

# After all commit messages have been checked, decide what to do if any error was found
if [ "$errors_found" -gt 0 ]; then
    # Message to the user
    echo "$errors_found commit message(s) contain forbidden message(s)."
    # Ask if he wants to bypass the commit message policy
    read -p "Do you want to proceed and push the changes? (y/n) " answer < /dev/tty
    # Check the answer
    if [ "$answer" != "y" ]; then
        # Message to the user that the push was aborted
        echo "The push was aborted. Please fix the commit messages and try again."
        # Exit with a non-zero status
        exit 1
    fi
fi