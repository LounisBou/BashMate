# Aliases for GIT
# Created by LounisBou

# GLOBAL VARIABLES

# List of workflow branches other than default branch (master|main)
work_branches=("staging")

# Reference branch for git-update-branch
ref_branch="main"

# Prefix for branches
branch_prefix_feature="feat"
branch_prefix_release="release"
branch_prefix_hotfix="hotfix"
branch_prefix_bugfix="bugfix"
branch_prefix_task="task"
branch_prefix_build="build"
branch_prefix_separator="-"

# Prefixes for commit messages (See : https://www.conventionalcommits.org/en/v1.0.0)
commit_prefix_build="build"            # Changes that affect the build system or external dependencies
commit_prefix_chore="chore"            # 
commit_prefix_ci="ci"                  # Changes to our CI configuration files and scripts
commit_prefix_docs="docs"              # Documentation only changes
commit_prefix_style="style"            # Changes that do not affect the meaning of the code
commit_prefix_refactor="refactor"      # A code change that neither fixes a bug nor adds a feature
commit_prefix_perf="perf"              # A code change that improves performance
commit_prefix_test="test"              # Adding missing tests or correcting existing tests
commit_prefix_separator=":"

# COMMANDS

# Get git repository default branch
function gdefault-branch(){
    # Check if .git exists
    if [ ! -d .git ]; then
        # Do nothing
        return
    fi
    # Check if master branch exists
    if git show-ref --verify --quiet refs/heads/master; then
        # Set default branch to master
        default_branch="master"
    else
        # Set default branch to main
        default_branch="main"
    fi
    # Return default branch
    echo $default_branch
}

# Git create repo
function gcreate(){
    git init -b main
    git add .
    git commit -m "Initial commit"
}
function gcreate-remote(){
    # Create repo on github
    gh repo create $* --source=. --private --confirm --remote --push
}
# Git global
alias ga="git add $*"
alias gc="git commit -m $*"
alias gp="git push origin $*"
alias gpl="git pull"
alias gs="git status"
alias gcl="git clone $*"
# Git branch
alias gb="git branch $*"
# Git log
function glg(){
    # Define variable nb_commits
    nb_commits=30
    # Check if $1 is not empty
    if [ ! -z "$1" ]
    then
        # Set $1 to nb_commits
        nb_commits=$1
    fi
    # Display git log
    git --no-pager log --graph --oneline --decorate --all -n $nb_commits
}
function gllc(){
    # Define variable nb_commits
    nb_commits=1
    # Check if $1 is not empty
    if [ ! -z "$1" ]
    then
        # Set $1 to nb_commits
        nb_commits=$1
    fi
    # Display git log
    git --no-pager log -$nb_commits
}
alias gdf="git diff"
# Git feature start
function gfs(){
    # Check if $1 is not empty
    if [ -z "$1" ]
    then
        # Display error message
        echo -e "${RED}Error: You must provide a feature name${NC}"
    else
        # Check if feature alternative prefix has been provided
        if [ ! -z "$2" ]
        then
            # Override branch prefix
            branch_prefix=$2
        else
            # Set default branch prefix
            branch_prefix=${branch_prefix_feature}
        fi
        # Feature branch name
        feature_branch=${branch_prefix}${branch_prefix_separator}$1
        # Checkout main branch
        git checkout $(gdefault-branch)
        # Pull main branch
        git pull
        # Create feature branch from main branch
        git checkout -b $feature_branch
    fi
}
# Git feature finish
function gff(){
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Workflow branches
    branches=($(gdefault-branch) ${work_branches[@]})
    # Check if current branch is in workflow branches
    if [[ " ${branches[@]} " =~ " ${current_branch} " ]]; then
        # Display error message
        echo -e "${RED}Error: You can't finish a workflow branch${NC}"
        return
    fi
    # Finish feature branch
    git checkout $(gdefault-branch)
    git pull
    git merge $current_branch
    git checkout $current_branch
    git push 
}

# Checkout
alias gco="git checkout $*"
function gcm(){
    # Checkout main branch
    git checkout $(gdefault-branch)
}
alias gcd="git checkout develop"
alias gct="git checkout tests"
alias gcp="git checkout prod"
alias gcpp="git checkout preprod"
alias gcs="git checkout staging"
# - Checkout local branch in interactive mode (Need fzf; see : https://github.com/junegunn/fzf)
function gco-local(){
    # Checkout branch in interactive mode, list all local branches and ask user to choose one
    git checkout $(git branch | fzf)
}
# - Checkout remote branch in interactive mode (Need fzf; see : https://github.com/junegunn/fzf)
function gco-remote(){
    # Fetch all branches
    git fetch --all
    # Checkout branch in interactive mode, list all remote branches and ask user to choose one
    git checkout $(git branch -r | fzf)
}
# - Checkout feature task branch
function gcft(){
    git checkout ${branch_prefix_feature}${branch_prefix_separator}${task_prefix}$*
}
# - Checkout feature branch
function gcf(){
    # Check if feature name is provided
    if [ -z "$1" ]
    then
        # Display error message
        echo -e "${RED}Error: You must provide a feature name${NC}"
    else
        # Check if feature alternative prefix has been provided
        if [ ! -z "$2" ]
        then
            # Override branch prefix
            branch_prefix=$2
        else
            # Set default branch prefix
            branch_prefix=${branch_prefix_feature}
        fi
        # Checkout feature branch
        git checkout ${branch_prefix}${branch_prefix_separator}$*
    fi
}
# - Checkout release branch
function gcr(){
    git checkout ${branch_prefix_release}${branch_prefix_separator}$*
}
# - Checkout hotfix branch
function gch(){
    git checkout ${branch_prefix_hotfix}${branch_prefix_separator}$*
}
# - Checkout bugfix branch
function gcb(){
    git checkout ${branch_prefix_bugfix}${branch_prefix_separator}$*
}
# Delete branches
# - Delete local branch
function gbrm(){
    git branch -d $*
}
# - Delete remote branch
function gbrm-remote(){
    # Delete remote branch
    git push origin --delete $*
}
# - Delete current branch
function gbrmc(){
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Checkout to default branch
    git checkout $(gdefault-branch)
    # Delete current branch
    git branch -d $current_branch
}
# - Delete remote current branch
function gbrmc-remote(){
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Delete remote current branch
    git push origin --delete $current_branch
}
# Stash
alias gst="git stash"
alias gstl="git stash list"
alias gstp="git stash pop"
alias gstc="git stash clear"
# Merge
function gmf(){
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Branch name
    branch_name=${branch_prefix_feature}${branch_prefix_separator}$*
    # Checkout on feature branch
    git checkout ${branch_name}
    # Update feature branch
    git pull
    # Checkout on current branch
    git checkout $(current_branch)
    # Merge feature branch
    git merge ${branch_name} -m "Merge ${branch_name} in ${current_branch}"
}
function gmft(){
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Branch name
    branch_name=${branch_prefix_feature}${branch_prefix_separator}$*
    # Checkout on feature task branch
    git checkout ${branch_name}
    # Update feature task branch
    git pull
    # Checkout on current branch
    git checkout $(current_branch)
    # Merge feature task branch
    git merge ${branch_name} -m "Merge ${branch_name} in ${current_branch}"
}
function gmergin(){
    # Retrieve current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Go to $1 branch
    git checkout $1
    # Merge current branch in $1 branch
    git merge $(current_branch) -m "Merge ${current_branch} in $1"
    # git add all
    git add .
    # git commit
    git commit -m "Merge ${current_branch} in $1"
    # Go back to current branch
    git checkout $(current_branch)
}
alias gmt="git mergetool"
# Get laster tag for branch
function gtag(){
    # Check if $1 is not empty
    if [ -z "$1" ]
    then
        # Set default branch name
        branch_name="$(gdefault-branch)"
    else
        # Set branch name
        branch_name=$1
    fi
    # Get last tag for current branch
    last_tag=$(git describe --tags `git rev-list --tags --max-count=1 $branch_name`)
    # Display last tag
    echo -e "${GREEN}Last tag for ${branch_name} branch is : ${last_tag} ${NC}"
}
# Push tag 
function gpt(){
    # Push all local tags
    git push origin --tags
    # Message user to call git after mep
    echo -e "${ORANGE}WARNING : You should call method 'git-after-mep' to update $(gdefault-branch) ${work_branch} branches ${NC}"
}
# Update $(gdefault-branch) ${work_branch} branch
function git-update(){
    # Retrieve current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Fetch all branches
    git fetch --all
    # List of branches to update
    branches=($(gdefault-branch) ${work_branches[@]})
    # Loop on branches
    for branch in "${branches[@]}"
    do
        # Checkout branch
        git checkout $branch
        # Pull branch
        git pull
    done
    # Checkout current branch
    git checkout $current_branch
    # Pull current branch
    git pull
}
# Update current branch by merging ref branch on it
function git-update-branch(){
    # Retrieve current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Branch to update
    branches=($(gdefault-branch) ${work_branches[@]})
    # Checkout ref branch
    git checkout $ref_branch
    # Pull branch
    git pull
    # Checkout current branch
    git checkout $current_branch
    # Pull current branch
    git pull
    # Merge ref branch in current branch
    git merge $ref_branch
    # Check if there is a conflict
    git diff --check
    # Ask user if he wants to continue
    read REPLY"?Do you want to continue ? (y/n) "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Commit merge
        git commit -m "Merge $ref_branch in $current_branch"
        # Push current branch
        git push
    fi
}
# After MEP
function git-after-mep(){
    # Retrieve current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # List of branches to update
    branches=($(gdefault-branch) ${work_branches[@]})
    # Loop on branches
    for branch in "${branches[@]}"
    do
        # Checkout branch
        git checkout $branch
        # Merge current branch in branch
        git merge $current_branch -m "Merge $current_branch in $branch"
        # Push branch
        git push
    done
    # Checkout current branch
    git checkout $current_branch
    # Push current branch
    git push
}
# Push current branch on a specific branch
function gpushon(){
    # Retrieve branch to push on
    branch_to_push_on=$1
    # Retrieve current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Add all files to commit
    ga .
    # Check if there is a commit message
    if [ -z "$2" ]
    then
        # Set default commit message
        commit_message="Push $current_branch on $branch_to_push_on"
    else
        # Set commit message
        commit_message=$2
    fi
    # Commit with message
    gc $commit_message
    # Push current branch
    gp $current_branch
    # Merge current branch in branch to push on
    gmergin $branch_to_push_on
    # Update $(gdefault-branch) ${work_branch[@]} branches
    git-update
    # Push on branch to push on
    gp $branch_to_push_on
}
# Manage merge conflicts
function git-conflicts(){
    # Retrieve current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Check if there is a conflict
    git diff --check
    # Ask user if he wants to continue
    read REPLY"?Do you want to continue ? (y/n) "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Commit merge
        git commit -m "Merge $ref_branch in $current_branch"
        # Push current branch
        git push
    fi
}
# Git rollback $1 commit
function git-rollback(){
    # Check if $1 is not empty
    if [ -z "$1" ]
    then
        # Set default number of commits
        nb_commits=1
    else
        # Set number of commits
        nb_commits=$1
    fi
    # Log the last $nb_commits commit(s)
    git --no-pager log --oneline --max-count=$nb_commits
    # Ask user if he is sure to rollback last commit
    read REPLY"?Do you want to rollback last $nb_commits commit(s) ? (y/n) "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Rollback last commit
        git reset --hard HEAD~$nb_commits
    else
        echo "Rollback aborted"
    fi
}
# Git rollback $1 commit
function git-log(){
    # Check if $1 is not empty
    if [ -z "$1" ]
    then
        # Set default number of commits
        nb_commits=1
    else
        # Set number of commits
        nb_commits=$1
    fi
    # Log the last $nb_commits commit(s)
    git --no-pager log --oneline --max-count=$nb_commits
}
# Git checkout to commit
function git-move-head(){
    # Get a list of commits using git log --oneline
    commit_list=$(git log --oneline)

    # If no commits are found, exit the script
    if [ -z "$commit_list" ]; then
        echo "No commits found."
        exit 1
    fi
    
    # Initialize an empty array
    commits=()

    # Read commit list line by line into an array
    while IFS= read -r line; do
        commits+=("$line")
    done <<< "$commit_list"

    # Use select to create a menu for checking out a commit
    PS3="Please select a commit to checkout (or 'q' to quit): "
    select commit_option in "${commits[@]}" "Quit"; do
        if [[ "$REPLY" = "q" ]] || [[ "$REPLY" = "Quit" ]]; then
            echo "Exiting..."
            break
        elif [[ -n "$commit_option" ]] && [[ "$REPLY" -le ${#commits[@]} ]]; then
            commit_hash=$(echo "$commit_option" | awk '{print $1}')
            echo "Checking out commit $commit_hash..."
            git checkout "$commit_hash"
            break
        else
            echo "Invalid option. Please try again."
        fi
    done
}   
# Infos
alias ginfo="git config --list"