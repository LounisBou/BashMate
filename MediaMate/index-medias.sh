#!/bin/bash

# Define the cache file path
cache_file="$HOME/.medias_cache"
# Define folders to exclude from indexing
excluded_folders=( ".actors" "Saison *" "trailers" "extrafanart" )

function index-medias() {
    # Clear the cache file before indexing
    : > "$cache_file" 

    # Construct the find command with exclusions dynamically
    exclude_expression=""
    for folder in "${excluded_folders[@]}"; do
        exclude_expression+=" -name '$folder' -prune -o"
    done

    # Loop through the disks and check if the medias folder exists
    for i in {1..4}; do
        local media_path="/Volumes/Disk${i}/medias"
        if [ -d "$media_path" ]; then
            echo "Checking $media_path..." >&2  # Output diagnostic messages to stderr
            echo "Indexing $media_path" >&2
            # Append only the directory paths to the cache file
            eval "find '$media_path' -type d \( $exclude_expression -print \) >> '$cache_file'"
        fi
    done
    
}

# Run the indexing function
index-medias
