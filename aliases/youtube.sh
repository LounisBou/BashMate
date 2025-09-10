#!/bin/zsh
# yt-dlp Aliases
# Download a song/album/playlist/artist from Spotify
# Created by Lounis Bouchentouf

# Install yt-dlp
function yt-dlp-install(){
    # Install dependencies
    brew install yt-dlp ffmpeg
}   

# Download playlist as mp3
function ytdl-mp3(){
    yt-dlp -x --audio-format mp3 -P "~/Music/Youtube" --audio-quality 0 -o "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" $*
}