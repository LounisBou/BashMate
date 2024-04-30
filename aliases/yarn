# Aliases for Yarn package manager
# Created by LounisBou

# GLOBAL VARIABLES

# COMMANDS

# Yarn commands
alias y="yarn $*"
alias yinstall="yarn install $*"
alias yadd="yarn add $*"
alias yadddev="yarn add --dev $*"
alias yremove="yarn remove $*"
alias yrun="yarn run $*"
alias yglobal="yarn global $*"

# Jest test
alias ytest="yarn test $*"

# Prettier
# - Format check
alias yprettier-check="yarn prettier:check $*"
# - Format fix (write)
alias yprettier-fix="yarn prettier:fix $*"

# ESLint
# - Lint check
alias ylint="yarn lint $*"

# Run Jest test, Prettier fix and ESLint lint
function ycheck() {
  yarn test && yarn prettier:fix && yarn prettier:check && yarn lint $*
}

# Vite server in dev mode
alias yserve="yarn dev $*"
# Vite server in prod mode
alias yserve-prod="yarn prod $*"

# Vite build
alias ybuild="yarn build $*"
alias ybuild-dev="yarn build --mode development $*"
alias ybuild-prod="yarn build --mode production $*"
