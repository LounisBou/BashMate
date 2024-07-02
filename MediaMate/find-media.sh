#!/bin/bash
# Find a media folder in media directories using .medias_cache

function find-media() {
    # Define the cache file path
    cache_file="$HOME/.medias_cache"

    # Check if the cache file exists and is not empty
    if [ ! -s "$cache_file" ]; then
        echo "Cache not found or empty. Please index the media folders first."
        echo "Run 'index-medias' to create the cache file."
        exit 1
    fi

    # Check if the user provided a folder name
    if [ -z "$*" ]; then
        echo "Usage: find-media <folder_name>"
        exit 1
    fi

    # Search for the foder name in the cache file
    grep -i "$*" "$cache_file"
}

# Run the find-media function
find-media "$@"