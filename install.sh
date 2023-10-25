#!/bin/bash

# Check if .zshrc exists
if [ -f "$HOME/.zshrc" ]; then
    # Add BashMate sourcing to .zshrc
    echo "source $(PWD)/bashmate.sh" >> ~/.zshrc
    echo "BashMate installed in .zshrc"
fi

# Check if .bashrc exists
if [ -f "$HOME/.bashrc" ]; then
    # Add BashMate sourcing to .bashrc
    echo "source $(PWD)/bashmate.sh" >> ~/.bashrc
    echo "BashMate installed in .bashrc"
fi

# Check if logo/logo.sh exists
if [ -f "logo/logo.sh" ]; then
    # Execute logo.sh
    ./logo/logo.sh
fi

# Provide instructions to the user
echo "BashMate installation completed."
echo "You may need to restart your shell or run 'source ~/.zshrc' or 'source ~/.bashrc' for the changes to take effect."