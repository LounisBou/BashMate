# Aliases for Composer package manager
# Created by LounisBou

# GLOBAL VARIABLES

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
ORANGE='\033[0;33m'
BLUE='\033[1;34m' # Light Blue
NC='\033[0m' # No Color

# COMMANDS

# Composer aliases
alias comp="composer $*"
alias comp-install="composer install"
alias comp-update="composer update"
alias comp-require="composer require"
alias comp-remove="composer remove"
alias comp-require-dev="composer require --dev"
alias comp-remove-dev="composer remove --dev"
alias comp-require-global="composer global require"
alias comp-remove-global="composer global remove"
alias comp-dump-autoload="composer dump-autoload"
