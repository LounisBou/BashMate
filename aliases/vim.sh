# Aliases for VIM.
# Created by LounisBou

# GLOBAL VARIABLES

# COMMANDS

# Install vim-plug (Vim plugin manager)
alias vim-plug-install="curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
# Install vim-plug (Vim plugin manager) for Neovim
alias nvim-plug-install="sh -c 'curl -fLo /Users/izno/.local/share/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'"

# Update .vimrc file with BashMate .vimrc file
alias vimrc-update="cd && rm .vimrc && cp BashMate/.vimrc .vimrc"
