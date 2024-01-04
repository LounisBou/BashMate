#!/usr/bin/env bash
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
    local target=$1
    local link_name=$2
    # Check target exists
    if [ ! -e "$link_name" ]; then
        # Create symlink
        ln -s "$target" "$link_name" || {
            echo "Failed to create symlink: $link_name from $target"
            return 1
        }
        echo "Created symlink: $link_name"
    else
        echo "Symlink already exists: $link_name"
    fi
}

# Create the versions directory if it doesn't exist
echo "# Link the php installed by Brew to $PHPENV_DIR"
for php_dir in "$CELLAR_DIR"/php*/[0-9]*.*; do
    # Check php dir exists
    if [ ! -d "$php_dir" ]; then
        continue
    fi
    # Check php bin exists
    phpPath="$php_dir/bin/php"
    if [ ! -f "$phpPath" ]; then
        continue
    fi
    # Create symlink
    version=$("$phpPath" -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION.".".PHP_RELEASE_VERSION;')
    create_symlink "$php_dir" "$PHPENV_DIR/$version" || true
done