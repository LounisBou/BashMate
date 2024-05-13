# Aliases for .env files management
# Created by LounisBou

# GLOBAL VARIABLES

# .env files name
env_file=".env"

# .env files suffixe
env_example_suffix=".example"
env_prod_suffix=".prod"
env_dev_suffix=".dev"
env_test_suffix=".test"
env_local_suffix=".local"

# COMMANDS

# Get environment file name from parameters
function env-file-name(){
    # Default .env file name
    env_file_name="$env_file"
    # For each argument set
    for arg in "$@"; do
        # check if the file with the suffix exists
        case "$arg" in
            "example")
                env_file_name="$env_file_name$env_example_suffix"
                ;;
            "prod")
                env_file_name="$env_file_name$env_prod_suffix"
                ;;
            "dev")
                env_file_name="$env_file_name$env_dev_suffix"
                ;;
            "test")
                env_file_name="$env_file_name$env_test_suffix"
                ;;
            "local")
                env_file_name="$env_file_name$env_local_suffix"
                ;;
            *)
                echo "{$RED}The suffix $arg is not valid.${NC}"
                return 1
                ;;
        esac
    done
    echo "$env_file_name"
}

# Check if the .env file exists
function env-exists() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    # check if the file exists
    if [ -f "$env_file_name" ]; then
        echo "{$GREEN}The $env_file_name file exists.${NC}"
    else
        echo "{$RED}The $env_file_name file does not exist.${NC}"
    fi
}

# Create a new environment file empty
function env-create() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    if [ -f "$env_file_name" ]; then
        echo "{$YELLOW}The $env_file_name file already exists.${NC}"
    else
        touch "$env_file"
        echo "{$GREEN}The $env_file_name file has been created.${NC}"
    fi
}

# Create a new environment file from an env.example file
function env-create-from-example() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    # Get the example file name
    env_example_file_name="$env_file$env_example_suffix"
    # check if the example file exists
    if [ -f "$env_example_file_name" ]; then
        cp "$env_example_file_name" "$env_file_name"
        echo "{$GREEN}The $env_file_name file has been created from the $env_example_file_name file.${NC}"
    else
        echo {$RED}The $env_example_file_name file does not exist.${NC}
    fi
}

# Copy the .env file to a new environment file
function env-copy() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    # check if the file exists
    if [ -f "$env_file_name" ]; then
        # Check if parameters contain the force option
        if [[ "$@" == *"--force"* ]]; then
            cp "$env_file" "$env_file_name"
            echo "{$GREEN}The $env_file_name file has been override.${NC}"
        else
            echo "{$YELLOW}The $env_file_name file already exists.${NC}"
        fi
    else
        cp "$env_file" "$env_file_name"
        echo "{$GREEN}The $env_file_name file has been copied.${NC}"
    fi
}

# Check if the .env file is up to date
function env-check() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    # Get the example file name
    env_example_file_name="$env_file$env_example_suffix"
    # check if the example file exists
    if [ -f "$env_example_file_name" ]; then
        # Check if the file is up to date
        if $(file-diff "$env_file_name" "$env_example_file_name"); then
            echo "${GREEN}The $env_file_name file is up to date.${NC}"
        else
            # Show the difference
            show-file-diff "$env_file_name" "$env_example_file_name"
        fi
    else
        echo "${RED}The $env_example_file_name file does not exist.${NC}"
    fi
}

# Check if the .env.example file is up to date with the .env file
function env-check-example() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    # Get the example file name
    env_example_file_name="$env_file$env_example_suffix"
    # check if the example file exists
    if [ -f "$env_example_file_name" ]; then
        # Check if the file is up to date ignoring whitespaces and blank lines
        if $(file-diff "$env_example_file_name" "$env_file_name"); then
            echo "${GREEN}The $env_example_file_name file is up to date.${NC}"
        else
            # Show the difference
            show-file-diff "$env_example_file_name" "$env_file_name"
        fi
    else
        echo "${RED}The $env_example_file_name file does not exist.${NC}"
    fi
}

# Update the .env file from an env.example file
function env-update() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    # Get the example file name
    env_example_file_name="$env_file$env_example_suffix"
    # Check if env file have different content from the example file
    if $(file-diff "$env_file_name" "$env_example_file_name"); then
        echo "${YELLOW}The $env_file_name file is already up to date.${NC}"
    else
        # Get array of the difference between the two files
        new_variables=$(file-diff-array "$env_file_name" "$env_example_file_name")
        # Add the new variables from the example file in the env file
        for new_variable in "${new_variables[@]}"; do
            echo "$new_variable" >> "$env_file_name"
        done
        echo "${GREEN}The $env_file_name file has been updated.${NC}"
    fi
}

# Update the .env.example file from the .env file
function env-update-example() {
    # Get environment file name from parameters
    env_file_name=$(env-file-name "$@")
    # Get the example file name
    env_example_file_name="$env_file$env_example_suffix"
    # Check if env file have different content from the example file
    if diff -w -B "$env_example_file_name" "$env_file_name" > /dev/null; then
        echo "${YELLOW}The $env_example_file_name file is already up to date.${NC}"
    else
        # Get array of the difference between the two files
        new_variables=$(file-diff-array "$env_example_file_name" "$env_file_name")
        # Add the new variables from the env file in the example file
        for new_variable in "${new_variables[@]}"; do
            echo "$new_variable" >> "$env_example_file_name"
        done
        echo "${GREEN}The $env_example_file_name file has been updated.${NC}"
    fi
}