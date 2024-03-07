#!/bin/bash

# Ask the user if they want to delete the merged branch
echo "--- Post merge branch deletion ---"

# Get the current branch name (branch_name is defined in the post-merge hook)
#branch_name=$(git branch | grep "*" | sed "s/\* //")

# Get the name of the branch that was just merged (merged_branch_name is defined in the post-merge hook)
#reflog_message=$(git reflog -1)
#merged_branch_name=$(echo $reflog_message | cut -d" " -f 4 | sed "s/://")

# List of branches to update
branches=()
# Get list of branches from main_branches.txt files (SCRIPT_DIR is defined in the post-merge hook)
while IFS= read -r line; do
    branches+=("$line")
done < "$SCRIPT_DIR/git/main_branches.txt"

# if the merged branch was in the list of branches, dont do anything
if [[ " ${branches[@]} " =~ " $merged_branch_name " ]]; then
    exit 1
fi

# Begin output
echo " "
echo "You've just merged the branch \"$merged_branch_name\" into \"$branch_name\". "

# Ask the question
read -p "Do you want to delete the \"$merged_branch_name\" branch? (y/N) " answer

# Check if the answer is a single lowercase Y
if [[ "$answer" == "y" ]]; then

	# Delete the local branch
	echo "Deleting local branch \"$merged_branch_name\""
	git branch -d $merged_branch_name

	# Delete the remote branch
	echo "Deleting remote branch"
	git push origin --delete $merged_branch_name
	exit 1
else
	echo "Did not delete the \"$merged_branch_name\" branch"
fi