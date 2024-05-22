# Aliases for GIT Flow
# Created by LounisBou

# Dependencies :
# - git aliases

# GLOBAL VARIABLES

# List of workflow branches other than default branch (master|main)
work_branches=("staging")

# Reference branch for git-update-branch
ref_branch="main"

# Prefix
feature_prefix="feat-"
release_prefix="release/"
hotfix_prefix="hotfix/"
bugfix_prefix="bugfix/"
task_prefix="task/"

# COMMANDS

# Git flow
alias gfi="git flow init"
alias gffs="git flow feature start $*"
alias gfff="git flow feature finish $*"
function gfrs(){
    # Call git update
    git-update
    # Create release branch
    git flow release start $*
}
function gfrf(){
    # Get default branch name
    default_branch=$(gdefault-branch)
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Check if current branch is a release branch
    if [[ $current_branch == ${release_prefix}* ]]
    then
        # Get release version
        release_version=$(echo $current_branch | cut -d '/' -f2)
        echo -e "${YELLOW}Finish release version: $release_version ${NC}"
        # Finish release
        git flow release finish $release_version
        # Push tags
        git push origin --tags
        # Message user to call git after mep
        echo -e "${ORANGE}WARNING : You should call method 'git-after-mep' to update ${default_branch} ${work_branches[@]} branches ${NC}"
        # Ask user if he wants to call git after mep
        read REPLY"?Do you want to call method 'git-after-mep' ? (y/n) "
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Call git after mep
            git-after-mep
        fi
    else
        # Message error current branch is not a release branch
        echo -e "${RED}Error: Current branch is not a release branch ${NC}"
    fi
}
function gfhs(){
    # Call git update
    git-update
    # Create hotfix branch
    git flow hotfix start $*
}
function gfhf(){
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Check if current branch is a hotfix branch
    if [[ $current_branch == ${hotfix_prefix}* ]]
    then
        # Get hotfix version
        hotfix_version=$(echo $current_branch | cut -d '/' -f2)
        echo "Finish hotfix version: $hotfix_version"
        # Finish hotfix
        git flow hotfix finish $hotfix_version
        # Push tags
        git push origin --tags
        # Message user to call git after mep
        echo -e "${ORANGE}WARNING : You should call method 'git-after-mep' to update $(gdefault-branch) ${work_branches[@]} branches ${NC}"
        # Ask user if he wants to call git after mep
        read REPLY"?Do you want to call method 'git-after-mep' ? (y/n) "
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Call git after mep
            git-after-mep
        fi
    else
        # Message error current branch is not a hotfix branch
        echo -e "${RED}Error: Current branch is not a hotfix branch${NC}"
    fi
}
function gfbs(){
    # Call git update
    git-update
    # Create bugfix branch
    git flow bugfix start $*
}
function gfbf(){
    # Get current branch name
    current_branch=$(git branch | grep \* | cut -d ' ' -f2)
    # Check if current branch is a bugfix branch
    if [[ $current_branch == ${bugfix_prefix}* ]]
    then
        # Get bugfix version
        bugfix_version=$(echo $current_branch | cut -d '/' -f2)
        echo "Finish bugfix version: $bugfix_version"
        # Finish bugfix
        git flow bugfix finish $bugfix_version
        # Push tags
        git push origin --tags
        # Message user to call git after mep
        echo -e "${ORANGE}WARNING : You should call method 'git-after-mep' to update $(gdefault-branch) ${work_branches[@]} branches ${NC}"
    else
        # Message error current branch is not a bugfix branch
        echo -e "${RED}Error: Current branch is not a bugfix branch${NC}"
    fi
}