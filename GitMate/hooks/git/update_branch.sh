#!/bin/bash

# Update current branch by merging develop branch on it
echo "--- Update current branch ---"

# Retrieve current branch name
current_branch=$(git branch | grep \* | cut -d ' ' -f2)
# Checkout develop branch
git checkout develop
# Pull develop branch
git pull
# Checkout current branch
git checkout $current_branch
# Pull current branch
git pull
# Merge develop branch on current branch
git merge develop
# Check if there is a conflict
git diff --check
# Ask user if he wants to continue
read -p "Do you want to continue (y/n) " answer < /dev/tty
# Check the answer
if [ "$answer" == "y" ]; then
    # Commit merge
    git commit -m "Merge develop in $current_branch"
    # Push current branch
    git push
fi
# Apply migration
php artisan migrate