#!/usr/bin/env zsh
# Path: BrewMate/includes/phpenv-link.sh
#
# This script links the php installed by Brew to ~/.phpenv/versions
#
# Usage: $ ./phpenv-link.sh
# This script must be re-run every time you install/update a version of php with Brew
#
# Inspired by yuki777/links-phps.bash
# See https://gist.github.com/yuki777/6244823b8aa8cf4457e97e6407ada5ad
#

# Define colors
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
# Light blue
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Exit with error if any command fails
set -euo pipefail

# Check brew is installed
if ! command -v brew >/dev/null 2>&1; then
    echo "Brew is not installed. Please install it first."
    exit 1
fi

# Constants
CELLAR_DIR=$(brew --prefix)/Cellar
PHPENV_DIR="$HOME/.phpenv/versions"
ERROR_MSG="Not found. brew package path: $CELLAR_DIR :("

# Check if cellar directory exists
if [ ! -d "$CELLAR_DIR" ]; then
    echo "$ERROR_MSG"
    exit 1
fi

# Function to create symlink
create_symlink() {
    # Arguments
    local target=$1
    local link_name=$2
    # Check target exists
    if [ ! -e "$link_name" ]; then
        # Message
        echo "Symlink not found: $link_name"
        # Create symlink
        echo "${YELLOW}Creating symlink: $link_name"
        ln -s "$target" "$link_name" || {
            echo "${RED}    Failed to create symlink: $link_name from $target${NC}"
            echo "${YELLOW}    $link_name is not a symlink, please remove it manually and re-run this script${NC}"
            return 1
        }
        echo ${GREEN}Created symlink: $link_name${NC}
    else
        # Remove symlink
        echo "${YELLOW}Removing symlink: $link_name"
        if [ -L "$link_name" ]; then
            rm "$link_name" || {
                echo "${RED}    Failed to remove symlink: $link_name${NC}"
                return 1
            }
            echo "${GREEN}  Removed symlink: $link_name${NC}"
        fi
        # Create symlink
        echo "${YELLOW}Creating symlink: $link_name${NC}"
        ln -s "$target" "$link_name" || {
            echo "${RED}    Failed to create symlink: $link_name from $target${NC}"
            return 1
        }
        echo "${GREEN}  Created symlink: $link_name${NC}"
    fi
    # Return success
    return 0
}

# Create the versions directory if it doesn't exist
echo "# Link the php installed by Brew to $PHPENV_DIR"
for php_dir in "$CELLAR_DIR"/php*/[0-9]*.*; do
    # Message
    echo "${YELLOW}Checking: $php_dir${NC}"
    # Check php dir exists
    if [ ! -d "$php_dir" ]; then
        continue
    fi
    echo "${GREEN}   Found: $php_dir${NC}"
    # Check php bin exists
    phpPath="$php_dir/bin/php"
    if [ ! -f "$phpPath" ]; then
        continue
    fi
    echo "${GREEN}   Found: $phpPath${NC}"
    # Get PHP version
    echo "${YELLOW}Check version with command : $phpPath -r 'echo PHP_MAJOR_VERSION.\".\".PHP_MINOR_VERSION.\".\".PHP_RELEASE_VERSION;'${NC}"
    version=$("$phpPath" -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION.".".PHP_RELEASE_VERSION;' 2>&1) || true
    # Remove warning message, keep only last line
    version=$(echo "$version" | tail -n 1)
    echo "${GREEN}  Version : $version${NC}"
    # If version is empty, skip
    if [ -z "$version" ]; then
        echo "${RED}    Failed to get version from $phpPath${NC}"
        continue
    fi
    # Create symlink
    create_symlink "$php_dir" "$PHPENV_DIR/$version" || true
    # Separator
    echo "----------------------------------------"
done