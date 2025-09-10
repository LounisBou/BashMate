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
# function zotify-install(){
#     brew install python@3 pipx ffmpeg git
#     pipx ensurepath
#     pipx install "git+https://github.com/zotify-dev/zotify.git@v1.0-dev" --suffix=-dev
#     export PATH=$PATH:$HOME/.local/bin
#     echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.zshrc
# }

# # Download a song/album/playlist/artist from Spotify
# function zotify-dl(){
#     zotify-dev --audio-format=mp3 --skip-duplicates --config="/Users/lounis/Library/Application Support/Zotify/config.json" -opt "{artist}/{album}/{song_name}.{ext}"  $*
# }

# Install zotify DraftKinner
function zotify-install(){
    # Install dependencies
    brew install python@3 pipx ffmpeg git
    pipx ensurepath
    # Install zotify from GitHub
    pipx install git+https://github.com/DraftKinner/zotify.git@v1.0.1 --force
    # Development version (alternative)
    # pipx install git+https://github.com/DraftKinner/zotify.git@dev
}

# Download a song/album/playlist/artist from Spotify
function zotify-dl(){
    # Retrieve parameters as url 
    local url="$1"
    shift  # Remove the first argument (URL) from the list
    # Check if url contains /intl-fr or /intl-en and remove it
    if [[ "$url" =~ /intl-(fr|en)/ ]]; then
        url="${url//\/intl-(fr|en)\//\/}"
    fi
    # Call zotify with the provided URL and remaining arguments
    zotify -m --audio-format=mp3 --skip-duplicates --config="/Users/lounis/Library/Application Support/Zotify/config.json" -opt "{artist}/{album}/{song_name}.{ext}" ${url} "$@"
}

# Download using zotify-dl foreach argument
function zdl(){
    local success_urls=()
    local failed_urls=()
    local total=0
    local error_delay=${ZDL_DELAY:-10}  # Default 10 second delay if error
    
    echo "Starting download of $# URLs..."
    echo "================================"
    
    # Loop over all arguments
    for url in "$@"; do
        ((total++))
        echo "[$total/$#] Processing: $url"
        
        # Create temporary file to capture output
        local temp_output="/tmp/zotify_output_$$_$total"
        
        # Run zotify-dl and capture exit code, redirect output to temp file
        zotify-dl "$url" > "$temp_output"
        local exit_code=$?
        
        # Read the captured output
        local output=""
        if [ -f "$temp_output" ]; then
            output=$(cat "$temp_output" 2>/dev/null)
            rm -f "$temp_output" 2>/dev/null
        fi
        
        # Check for success: exit code 0 AND no "Audio key error" in output
        if [ $exit_code -eq 0 ] && [[ ! "$output" =~ "Audio key error" ]]; then
            echo "✅ SUCCESS: $url"
            success_urls+=("$url")
        else
            if [[ "$output" =~ "Audio key error" ]]; then
                echo "❌ FAILED (Audio key error): $url"
            else
                echo "❌ FAILED (Exit code: $exit_code): $url"
            fi
            # Show output if available
            if [ -n "$output" ]; then
                echo "Output: $output"
            else
                echo "No output captured."
            fi
            failed_urls+=("$url")
            # Add delay between downloads if error (except for the last one)
            if [ $total -lt $# ]; then
                echo "⏳ Waiting ${error_delay} seconds before next download..."
                sleep $error_delay
            fi
        fi

        echo "--------------------------------"
    done
    
    # Summary
    echo "SUMMARY:"
    echo "========"
    echo "Total processed: $total"
    echo "Successful: ${#success_urls[@]}"
    echo "Failed: ${#failed_urls[@]}"
    
    if [ ${#success_urls[@]} -gt 0 ]; then
        echo ""
        echo "✅ SUCCESSFUL URLs:"
        for url in "${success_urls[@]}"; do
            echo "  - $url"
        done
    fi
    
    if [ ${#failed_urls[@]} -gt 0 ]; then
        echo ""
        echo "❌ FAILED URLs:"
        for url in "${failed_urls[@]}"; do
            echo "  - $url"
        done
        # Print command to retry failed URLs
        echo ""
        echo "You can retry failed URLs with:"
        echo "zdl ${failed_urls[@]}"
        return 1  # Return error code if there were failures
    fi
    
    return 0  # Return success code if all succeeded
}

# Retry zdl call while everything success or max_retries attempt reach.
function zdl-retry(){
    local max_retries=${ZDL_MAX_RETRIES:-5}  # Default to 5 retries, configurable
    local retry_delay=60  # 60 seconds between retries
    local retry_count=0
    
    echo "Starting zdl-retry with $# URLs (max $max_retries retries)"
    echo "============================================================"
    
    while [ $retry_count -lt $max_retries ]; do
        ((retry_count++))
        
        if [ $retry_count -eq 1 ]; then
            echo "🚀 Initial attempt with $# URLs"
        else
            echo "🔄 Retry attempt #$retry_count"
            echo "⏳ Waiting ${retry_delay} seconds before retry..."
            # sleep during delay x retry count
            sleep $((retry_delay * retry_count))
        fi
        echo "============================================================"
        
        # Call zdl with all URLs
        if zdl "$@"; then
            echo "🎉 All URLs processed successfully!"
            return 0
        else
            echo "❌ Some URLs failed in attempt $retry_count"
            
            if [ $retry_count -ge $max_retries ]; then
                echo "⚠️  Maximum retries ($max_retries) reached."
                break
            fi
        fi
        echo "============================================================"
    done
    
    # Final summary
    echo ""
    echo "🏁 FINAL SUMMARY:"
    echo "=================="
    echo "Total retry attempts: $retry_count"
    echo "❌ Some URLs still failing after $max_retries attempts"
    echo "💡 You can check which ones failed in the last zdl output above"
    
    return 1  # Exit with error code
}

# Remove "Disk 1" folders
function zdl-rm-disk(){
    for disc_dir in **/Disc\ 1(/); do mv "$disc_dir"/*.mp3 "${disc_dir:h}/" 2>/dev/null; rmdir "$disc_dir" 2>/dev/null; done
}