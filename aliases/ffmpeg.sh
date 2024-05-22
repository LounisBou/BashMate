# Aliases for ffmpeg.
# Created by LounisBou

# DEPENDENCIES
# ffmpeg
# convert

# GLOBAL VARIABLES

# COMMANDS

# Convert video to gif
function video-to-gif(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Convert video to gif
    ffmpeg -i $1 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 -loop 0 - gif:- | convert -layers Optimize - ${file_name}.gif
}

# Convert video to gif with custom fps
function video-to-gif-fps(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Convert video to gif
    ffmpeg -i $1 -vf "fps=$2,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 -loop 0 - gif:- | convert -layers Optimize - ${file_name}.gif
}

# Concat mp3 in folder into one mp3 file
function concat-mp3(){
    # Check if path passed as argument
    if [ -n "$1" ]; then
        # Get path
        folder_path=$1
    else
        # Get current folder path
        folder_path=${PWD}
    fi
    # Get current folder name from path
    folder_name=$(basename -- "$folder_path")
    # Concat mp3 files
    ffmpeg -i "concat:$(ls -1 $folder_path/*.mp3 | tr '\n' '|')" -acodec copy ${folder_name}.mp3
}

# Loop over all folders in current folder and concat mp3 in each folder into one mp3 file
function concat-mp3-all(){
    # Loop over all folders in current folder
    for folder in */; do
        # Concat mp3 files in folder
        concat-mp3 $folder
    done
}

# Concat mp4 in folder into one mp4 file
function concat-mp4(){
    # Check if path passed as argument
    if [ -n "$1" ]; then
        # Get path
        folder_path=$1
    else
        # Get current folder path
        folder_path=${PWD}
    fi
    # Get current folder name from path
    folder_name=$(basename -- "$folder_path")
    # Concat mp4 files
    ffmpeg -i "concat:$(ls -1 $folder_path/*.mp4 | tr '\n' '|')" -c copy ${folder_name}.mp4
}

# Extract audio from video
function extract-audio(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Extract audio from video
    ffmpeg -i $1 -vn -acodec copy ${file_name}.aac
}

# Extract video from video
function extract-video(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Extract video from video
    ffmpeg -i $1 -an -vcodec copy ${file_name}.mp4
}