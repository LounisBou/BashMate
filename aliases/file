# Aliases for files management
# Created by LounisBou

# GLOBAL VARIABLES

# COMMANDS

# Create a new file and open it with vim
function file-create() {
    touch $1 && vim $1
}

# Find a file in the current directory recursively
function file-find() {
    # Check if the argument is empty
    if [ -z $1 ]; then
        echo "${YELLOW}Please provide a file name to search for.${NC}"
        return 1
    fi
    # Check if file exists
    if [ ! -e $1 ]; then
        echo "${RED}File not found.${NC}"
        return 1
    fi
    # Print the file relative path
    find . -name $1
}

# Check if a file contains a string
function file-contains() {
    # Check if the argument is empty
    if [ -z $1 ]; then
        echo "${YELLOW}Please provide a string to search for.${NC}"
        return 1
    fi
    # Check if the argument is empty
    if [ -z $2 ]; then
        echo "${YELLOW}Please provide a file name.${NC}"
        return 1
    fi
    # Check if file exists
    if [ ! -e $2 ]; then
        echo "${RED}File not found.${NC}"
        return 1
    fi
    # Check if the file contains the string
    if grep -q $1 $2; then
        # Show the line containing the string, with the line number and previous and next lines
        grep -n -C 1 $1 $2
    else
        echo "${YELLOW}The file does not contain the string.${NC}"
    fi
}

# Check if a file is empty
function file-is-empty() {
    # Check if the argument is empty
    if [ -z $1 ]; then
        echo "${YELLOW}Please provide a file name.${NC}"
        return 1
    fi
    # Check if file exists
    if [ ! -e $1 ]; then
        echo "${RED}File not found.${NC}"
        return 1
    fi
    # Check if the file is empty
    if [ -s $1 ]; then
        echo "${RED}The file is not empty.${NC}"
    else
        echo "${GREEN}The file is empty.${NC}"
    fi
}

# File comparison
function file-diff(){
    if diff -i -b <(sed '/^[[:space:]]*$/d;s/[[:space:]]\+/ /g;s/[[:space:]]*$//;s/^\([[:space:]]*\)//' $1 | tr '[:upper:]' '[:lower:]') \
         <(sed '/^[[:space:]]*$/d;s/[[:space:]]\+/ /g;s/[[:space:]]*$//;s/^\([[:space:]]*\)//' $2 | tr '[:upper:]' '[:lower:]') > /dev/null;
    then
        return 0
    else
        return 1
    fi
}

# Get array of differences between two files
function file-diff-array() {
    diff -i -b <(sed '/^[[:space:]]*$/d;s/[[:space:]]\+/ /g;s/[[:space:]]*$//;s/^\([[:space:]]*\)//' $1 | tr '[:upper:]' '[:lower:]') \
         <(sed '/^[[:space:]]*$/d;s/[[:space:]]\+/ /g;s/[[:space:]]*$//;s/^\([[:space:]]*\)//' $2 | tr '[:upper:]' '[:lower:]') | grep -E '^[<>]' | sed 's/^[<>]//'
}

# Show the differences between two files
function file-diff-show() {
    # Get the differences between the two files
    file_diff_array=($(file-diff-array $@))
    # Check if the array is empty
    if [ ${#file_diff_array[@]} -eq 0 ]; then
        echo "${GREEN}No differences found.${NC}"
        return 0
    fi
    # Show the differences
    echo "Differences found :"
    for line in "${file_diff_array[@]}"; do
        echo "  ${YELLOW}${line}${NC}"
    done
}

# Compare two files content
function file-compare() {
    # Check if the argument is empty
    if [ -z $1 ]; then
        echo "${YELLOW}Please provide a primary file name.${NC}"
        return 1
    fi
    # Check if the argument is empty
    if [ -z $2 ]; then
        echo "${YELLOW}Please provide a secondary file name.${NC}"
        return 1
    fi
    # Check if file exists
    if [ ! -e $1 ]; then
        echo "${RED}$1 : File not found.${NC}"
        return 1
    fi
    # Check if file exists
    if [ ! -e $2 ]; then
        echo "${RED}$2 : File not found.${NC}"
        return 1
    fi
    # Check the files content, ignore : blank lines, spaces, tabs, case, line endings, and trailing whitespaces
    if $(file-diff $@); then
        echo "${GREEN}Files are identical.${NC}"
        return 0
    else
        # Show the differences
        file-diff-show $@
        return 1
    fi
}
