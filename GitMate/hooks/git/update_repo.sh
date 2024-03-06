#!/bin/bash

# Update repository with the latest local changes
echo "--- Update Repository ---"

# List of branches to update
branches=()
# Get list of branches from main_branches.txt files (SCRIPT_DIR is defined in the pre-* hook)
while IFS= read -r line; do
    branches+=("$line")
done < "$SCRIPT_DIR/git/main_branches.txt"

# Retrieve current branch name
current_branch=$(git branch | grep \* | cut -d ' ' -f2)

# Fetch all branches
git fetch --all

# Loop on branches
for branch in "${branches[@]}"
do
    # Checkout branch
    git checkout $branch
    # Push branch
    git push
done

# Checkout current branch
git checkout $current_branch
# Push current branch
git push