#!/bin/zsh
# Zotify Aliases
# Download a song/album/playlist/artist from Spotify
# Created by Lounis Bouchentouf

# DEPENDENCIES
# Python 3.9 or greater
# pipx (https://github.com/pypa/pipx)
# FFmpeg
# zotify (https://github.com/zotify-dev/zotify?tab=readme-ov-file)

# Install zotify
function zotify-install(){
    brew install python@3 pipx ffmpeg git
    pipx ensurepath
    pipx install https://get.zotify.xyz
    export PATH=$PATH:$HOME/.local/bin
    echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.zshrc
}

# Download a song/album/playlist/artist from Spotify
function zotify-dl(){
    zotify --root-path=. --output={artist}/{album}/{song_name}.{ext} --download-format=mp3 --download-lyrics=false $*
}

