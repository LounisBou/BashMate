# Aliases for ffmpeg.
# Created by LounisBou

# DEPENDENCIES
# ffmpeg
# ffplay
# ffprobe
# convert

# GLOBAL VARIABLES

# COMMANDS

# Play video
function ffmpeg-play-video(){
    # Play video
    ffplay $1
}

# Play audio
function ffmpeg-play-audio(){
    # Play audio
    ffplay $1
}

# Convert video to gif
function ffmpeg-video-to-gif(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Convert video to gif
    ffmpeg -i $1 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 -loop 0 - gif:- | convert -layers Optimize - ${file_name}.gif
}

# Convert video to gif with custom fps
function ffmpeg-video-to-gif-fps(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Convert video to gif
    ffmpeg -i $1 -vf "fps=$2,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 -loop 0 - gif:- | convert -layers Optimize - ${file_name}.gif
}

# Concat mp3 in folder into one mp3 file
function ffmpeg-concat-mp3(){
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
function ffmpeg-concat-mp3-all(){
    # Loop over all folders in current folder
    for folder in */; do
        # Concat mp3 files in folder
        ffmpeg-concat-mp3 $folder
    done
}

# Concat mp4 in folder into one mp4 file
function ffmpeg-concat-mp4(){
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
function ffmpeg-extract-audio(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Extract audio from video
    ffmpeg -i $1 -vn -acodec copy ${file_name}.aac
}

# Extract video from video
function ffmpeg-extract-video(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Extract video from video
    ffmpeg -i $1 -an -vcodec copy ${file_name}.mp4
}

# Extract frames from video
function ffmpeg-extract-frames(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Check if fps passed as argument
    if [ -n "$2" ]; then
        # Get fps
        fps=$2
    else
        # Set default fps to 1
        fps=1
    fi
    # Check if resolution passed as argument
    if [ -n "$3" ]; then
        # Get resolution
        resolution=$3
    else
        # Set default resolution to video resolution
        resolution=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 $1)
    fi
    # Define parameters
    parameters="fps=${fps}"
    # Check if resolution is not empty
    if [ -n "$resolution" ]; then
        # Add resolution to parameters
        parameters="${parameters},scale=${resolution}:flags=lanczos"
    fi
    # Extract frames from video
    ffmpeg -i $1 -vf "${parameters}" ${file_name}_%04d.png
}

# Convert audio from one format to another
function ffmpeg-convert-audio(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Get new format
    new_format=$2
    # Convert audio to new format
    ffmpeg -i $1 ${file_name}.${new_format}
}

# Convert video from one format to another
function ffmpeg-convert-video(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Get new format
    new_format=$2
    # Convert video to new format
    ffmpeg -i $1 ${file_name}.${new_format}
}

# Change audio volume
function ffmpeg-change-volume(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Get volume
    volume=$2
    # Change audio volume
    ffmpeg -i $1 -af "volume=${volume}" ${file_name}_volume${volume}.mp3
}

# Merge audio and video
function ffmpeg-merge-audio-video(){
    # Retrieve audio file name without extension
    audio_file_name=$(basename -- "$1")
    # Retrieve video file name without extension
    video_file_name=$(basename -- "$2")
    # Merge audio and video
    ffmpeg -i $1 -i $2 -c:v copy -c:a aac -strict experimental ${audio_file_name}_${video_file_name}.mp4
}

# Change video resolution
function ffmpeg-change-resolution(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Get resolution
    resolution=$2
    # Change video resolution
    ffmpeg -i $1 -vf scale=${resolution} ${file_name}_resolution${resolution}.mp4
}

# Change video speed
function ffmpeg-change-speed(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Get speed
    speed=$2
    # Change video speed
    ffmpeg -i $1 -filter:v "setpts=${speed}*PTS" ${file_name}_speed${speed}.mp4
}

# Compress video
function ffmpeg-compress-video(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Check if quality passed as argument
    if [ -n "$2" ]; then
        # Get quality
        quality=$2
    else
        # Set default quality to 23
        quality=23
    fi
    # Compress video
    ffmpeg -i $1 -vf scale=iw*0.5:ih*0.5 -c:v libx264 -crf ${quality} -preset slow -c:a aac -b:a 128k ${file_name}_quality${quality}.mp4
}

# Compress audio
function ffmpeg-compress-audio(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Check if quality passed as argument
    if [ -n "$2" ]; then
        # Get quality
        quality=$2
    else
        # Set default quality to 128k
        quality=128k
    fi
    # Compress audio
    ffmpeg -i $1 -c:a aac -b:a ${quality} ${file_name}_quality${quality}.mp3
}

# Add poster to video
function ffmpeg-add-poster(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Add poster to video
    ffmpeg -i $1 -i $2 -c copy -map 0 -map 1 -disposition:1 attached_pic ${file_name}_poster.mp4
}

# Add watermark to video
function ffmpeg-add-watermark(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Add watermark to video
    ffmpeg -i $1 -i $2 -filter_complex "overlay=10:10" ${file_name}_watermark.mp4
}

# Add subtitles to video
function ffmpeg-add-subtitles(){
    # Retrieve file name without extension
    file_name=$(basename -- "$1")
    # Add subtitles to video
    ffmpeg -i $1 -i $2 -c copy -c:s mov_text ${file_name}_subtitles.mp4
}
