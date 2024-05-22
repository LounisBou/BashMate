# Aliases for sips (Scriptable image processing system) on MacOS.
# Created by LounisBou

# DEPENDENCIES
# sips

# GLOBAL VARIABLES
export IMAGES_EXTENSIONS="png,jpg,jpeg,tiff,tif,gif,heic,heif,bmp"

# COMMANDS

# Resize all images in a folder
function sips-resize(){
    # Get first argument as working path
    working_path=$1
    # Get wanted size
    wanted_width=$2
    # Check if resize wanted on height or width ($3 --height or --width)
    if [ $3 == "--height" ]; then
        sips_arguements="--resampleHeight"
    else
        sips_arguements="--resampleWidth"
    fi
    # Check if working path file or folder
    if [ -f $working_path ]; then
        # Get file base name
        file_base_name=$(basename -- "$working_path")
        # Get file extension
        file_extension="${file_base_name##*.}"
        # Resize image if it's a file
        sips $sips_arguements $wanted_width $working_path --out $file_base_name-width-$wanted_width.$file_extension
    else
        # Resize all images in a folder
        for ext in $(echo $IMAGES_EXTENSIONS | tr "," "\n"); do
            for image in $1/*.$ext; do
                # Get file base name
                file_base_name=$(basename -- "$image")
                # Get file extension
                file_extension="${file_base_name##*.}"
                # Resize image
                sips $sips_arguements $wanted_width $image --out $1/$file_base_name-width-$wanted_width.$file_extension
            done
        done
    fi
}
function sips-resize-height(){
    # Call sips-resize with height argument
    sips-resize $1 $2 --height
}
function sips-resize-width(){
    # Call sips-resize with width argument
    sips-resize $1 $2 --width
}

# Convert image to another format
function sips-convert-format(){
    # Get first argument as working path
    working_path=$1
    # Get wanted format
    wanted_format=$2
    # Check if working path file or folder
    if [ -f $working_path ]; then
        # Get file base name
        file_base_name=$(basename -- "$working_path")
        # Get file extension
        file_extension="${file_base_name##*.}"
        # Convert image if it's a file
        sips -s format $wanted_format $working_path --out $file_base_name.$wanted_format
    else
        # Convert all images in a folder to another format
        sips -s format $wanted_format $working_path/*.png
    fi
}

# Rotate image by angle (90, 180, 270)
function sips-rotate-image(){
    # Get first argument as working path
    working_path=$1
    # Get wanted angle
    wanted_angle=$2
    # Check if working path file or folder
    if [ -f $working_path ]; then
        # Get file base name
        file_base_name=$(basename -- "$working_path")
        # Get file extension
        file_extension="${file_base_name##*.}"
        # Rotate image if it's a file
        sips -r $wanted_angle $working_path --out $file_base_name-rotated-$wanted_angle.$file_extension
    else
        # Rotate all images in a folder
        for ext in $(echo $IMAGES_EXTENSIONS | tr "," "\n"); do
            for image in $1/*.$ext; do
                # Get file base name
                file_base_name=$(basename -- "$image")
                # Get file extension
                file_extension="${file_base_name##*.}"
                # Rotate image
                sips -r $wanted_angle $image --out $1/$file_base_name-rotated-$wanted_angle.$file_extension
            done
        done
    fi
}
