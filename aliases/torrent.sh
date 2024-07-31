# Aliases for torrent management
# Created by LounisBou

# GLOBAL VARIABLES

# ToSort directory
TOSORT_PATH="/Users/izno/Downloads/A TRIER"

# ToSort sub-directories
TOSORT_MOVIES="001 FILMS"
TOSORT_TVSHOWS="002 SERIES"

# List of medias extensions
MEDIA_EXTENSIONS=(
    "avi" "mkv" "mp4" "mpg" "mpeg" "mov" "wmv" "flv" "webm" "m4v" 
    "3gp" "3g2" "asf" "rm" "swf" "vob" "ts" "m2ts" "mts" "m2t" 
    "m4p" "m4b" "m4r" "m4a" "m4v" "f4v" "f4a" "f4b" "f4p" "f4r"
    "ogg" "ogv" "oga" "ogx" "ogm" "spx" "opus" "flac" "wav" "mp3"
    "wma" "aac" "ac3" "dts" "pcm" "mka" "mks" "weba" "webm" "amr"
    "ra" "rm" "ram" "rmvb" "rpm" "rt" "rp" "smi" "smil" "m3u" "m3u8"
    "pls" "xspf" "asx" "wax" "wvx" "wmx" "wpl" "b4s" "kpl" "pla"
)

# List of characters to delete from file names
CHARS_TO_DELETE=("5.1" "4.0" "." "-" "_" "[" "]" "{" "}" "~" "+" "(" ")" "!")

# List of words to delete from file names
WORDS_TO_DELETE=(
    "1080"
    "1080i"
    "1080p"
    "10bit"
    "1920x1080"
    "2160p"
    "2vf"
    "480p"
    "720p"
    "7sins"
    "4k"
    "4klight"
    "6ch"
    "aac"
    "aaclc"
    "abcollection"
    "ac 3"
    "ac3"
    "acc"
    "acool"
    "amzn"
    "ark01"
    "avc"
    "bbc"
    "bdrip"
    "benh4"
    "bit"
    "bluray"
    "bluray1080p"
    "brrip"
    "buret"
    "ccats"
    "ch"
    "chris44"
    "custom"
    "darkjuju"
    "dd"
    "ddp"
    "directors cut"
    "dl"
    "dolby vision"
    "dread team"
    "dts"
    "dvdrip"
    "dvd rip"
    "eaulive"
    "en"
    "eng"
    "extended"
    "extreme"
    "fasandraeberne"
    "final cut"
    "flaskepost"
    "fr"
    "fre"
    "french"
    "french(vff)"
    "frosties"
    "ftmvhd"
    "fw"
    "gbx"
    "ght"
    "ghz"
    "gismo65"
    "gwen"
    "h264"
    "h265"
    "h4s5s"
    "hd"
    "hdl"
    "hdlight"
    "hdma"
    "hdr"
    "hdtv"
    "he"
    "hevc"
    "hush"
    "integral"
    "integrale"
    "internal"
    "jiheff"
    "k7"
    "kaf"
    "kfl"
    "kvinden"
    "lazarus"
    "lcds"
    "libertad"
    "luminus"
    "mhd"
    "mhdgz"
    "mkv"
    "mm91"
    "moe"
    "mtl666"
    "multi"
    "multi3"
    "nf"
    "noex"
    "nobodyperfect"
    "non censurée"
    "notag"
    "nyu"
    "owii"
    "p4t4t3"
    "pop"
    "pophd"
    "Portos"
    "portos"
    "qtz"
    "remastered"
    "romkent"
    "se7en"
    "serqph"
    "shc23"
    "slayer"
    "slay3r"
    "srt"
    "stereo"
    "tf"
    "title1"
    "tonyk"
    "tr"
    "truefrench"
    "trunkdu92"
    "tvwh0res"
    "unrated"
    "uptopol"
    "utt"
    "version"
    "vf"
    "vf2"
    "vff"
    "vfi"
    "vfq"
    "vlis"
    "vmpp"
    "vo"
    "vof"
    "vost"
    "vostfr"
    "web"
    "web dl"
    "webdl"
    "webrip"
    "x264"
    "x265"
    "xvid"
    "zeusfaber"
    "zone80"
    "zza"
)

# COMMANDS

# - CHECKS

# Check if a file is a media file
function torrent-is-media() {
    # Get the file extension
    ext="${1##*.}"
    # Check if the extension is in the list of media extensions
    for media in "${MEDIA_EXTENSIONS[@]}"; do
        if [[ "$media" == "$ext" ]]; then
            return 0
        fi
    done
    return 1
}

# Check if a file is a tv show
function torrent-is-tv-show() {
    # Strtolower
    base=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    # Check if file is media
    if ! torrent-is-media "$base"; then
        echo "Not a media file"
        return 1
    fi
    # Check if the file name contains a season and an episode
    if [[ "$base" =~ s[0-9]{2}e[0-9]{2} ]]; then
        return 0
    else
        return 1
    fi
}

# Check if directory contains a tv show
function torrent-dir-is-tv-show() {
    # Get the directory name
    dir="${1}"
    # Check if the directory exists
    [ -d "${dir}" ] || return 1
    # Check if the directory contains a tv show
    for file in "${dir}"/*; do
        # Only check files
        if [ -f "${file}" ]; then
            # Only check if not starting with a dot
            if [[ "${file}" != .* ]]; then
                # Check if the file is a tv show
                if torrent-is-tv-show "${file}"; then
                    return 0
                fi
            fi
        fi
    done
    return 1
}

# - CLEAN

# Clear directory name last slash
function torrent-dir-clean() {
    # Get the directory name
    dir="${1}"
    # Remove the last slash if it exists
    dir="${dir%/}"
    # Return the cleaned directory name
    echo "${dir}"
}

# Clean file names from unwanted characters
function torrent-clean-chars() {
    # Get the file name without the extension
    base="$1"
    # Clean the file name
    for char in $CHARS_TO_DELETE; do
        # Replace the character by a space
        base="${base//${char}/ }"
    done
    # Return new file name
    echo "${base}"
}

# Clean file names from unwanted words
function torrent-clean-words() {
    # Get the file name without the extension
    base="$1 "
    # Clean the file name
    for word in $WORDS_TO_DELETE; do
        # Replace the word by nothing if there is a space before and after or at the beginning or at the end
        base="${base// ${word} / }"
    done
    # Return new file name
    echo "${base}"
}

# Clean file names from unwanted characters and words
function torrent-clean() {
    # Strtolower
    base=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    # Check if file is tv show
    if torrent-is-tv-show "$1"; then
        # Keep only part before season and episode
        base=$(echo "$base" | sed -E 's/(.*)\.s[0-9]{2}e[0-9]{2}.*/\1/')
    else
        # Get the file name without the extension
        base="${base%.*}"
    fi
    # Replace forbidden characters by spaces
    base=$(torrent-clean-chars "$base")
    # Replace forbidden words by nothing
    base=$(torrent-clean-words "$base")
    # Remove leading and trailing spaces
    base=$(echo "$base" | xargs)
    # Return new file name
    echo "${base}"
}

# - PACK

# Pack = Put a file into a subdirectory with the same name cleaned
function torrent-pack() {
    # Check if the file exists
    if [ -f "$1" ]; then
        # Clean the file name
        base=$(torrent-clean "$1")
        # Create a directory with the base name if it does not exist
        [ -d "$base" ] || mkdir "$base"
        echo "${YELLOW}Packing ${1} into ${base} ${NC}"
        # Move the file into the directory
        mv "$1" "$base"
    fi
}

# Pack all files of the current directory
function torrent-pack-all() {
    for file in *; do
        # Only pack files
        [ -f "$file" ] &&
        torrent-pack "$file"
    done
}

# Pack all files of the current directory that are not tv shows
function torrent-pack-movies() {
    for file in *; do
        # Only pack files
        [ -f "$file" ] &&
        # Only pack files that are not tv shows
        ! torrent-is-tv-show "$file" &&
        # Pack the file
        torrent-pack "$file"
    done
}

# Pack all files of the current directory that are tv shows
function torrent-pack-tvshow() {
    for file in *; do
        # Only pack files
        [ -f "$file" ] &&
        # Only pack files that are tv shows
        torrent-is-tv-show "$file" &&
        # Pack the file
        torrent-pack "$file"
    done
}

# - UNPACK

# Unpack = Move all files from a directory to the parent directory
function torrent-unpack() {
    echo "${YELLOW}Unpacking ${1} ${NC}"
    # Get the directory name
    dir="${1}"
    # Clear the directory name
    dir=$(torrent-dir-clean "${dir}")
    # Clear files in the directory
    torrent-clear-non-media "${dir}"
    # Move all files from the directory to the parent directory
    for file in "${dir}"/*; do
        # Only move files
        [ -f "${file}" ] &&
        # Move the file
        mv "${file}" .
    done
    # Remove the directory
    rm -rf "${dir}"
}

# - CLEAR

# Remove non media files from a directory
function torrent-clear-non-media() {
    # Get the directory name
    dir="${1}"
    # Check if the directory exists
    [ -d "${dir}" ] || return 1
    # Remove all files that are not media files
    for file in "${dir}"/*; do
        # Only remove files
        [ -f "${file}" ] &&
        # Only remove files that are not media files
        ! torrent-is-media "${file}" &&
        # Remove the file
        rm "${file}"
    done
}

# - PACK/UNPACK

# Unpack then pack elements of the current directory
function torrent-unpack-pack() {
    # Get all directories in the current directory
    for element in *; do
        # Only unpack directories
        if [ -d "${element}" ]; then
            # Not starting with a dot
            if [[ "${element}" != .* ]]; then
                # Only unpack if not starting with a 0
                if [[ "${element}" != 0* ]]; then
                    # Unpack the directory
                    torrent-unpack "${element}"
                fi
            fi
        fi
    done
    # Get all files in the current directory
    for file in *; do
        # Only pack files
        if [ -f "${file}" ]; then
            # Only pack if not starting with a dot
            if [[ "${file}" != .* ]]; then
                # Pack the file
                torrent-pack "${file}"
            fi
        fi
    done
}

# - SORT

# Sort a directory between movies and tv shows
function torrent-sort(){
    # Check if the directory exists
    [ -d "${1}" ] || return 1
    # Check if the directory contains a tv show
    if torrent-dir-is-tv-show "${1}"; then
        # Move the directory to the tv shows directory
        echo "${YELLOW}Moving ${1} to ${TOSORT_TVSHOWS} ${NC}"
        mv "${1}" "${TOSORT_TVSHOWS}"
    else
        # Move the directory to the movies directory
        echo "${YELLOW}Moving ${1} to ${TOSORT_MOVIES} ${NC}"
        mv "${1}" "${TOSORT_MOVIES}"
    fi
}

# Sort all directories of the current directory
function torrent-sort-dirs() {
    # Get all directories in the current directory
    for element in *; do
        # Only sort directories
        if [ -d "${element}" ]; then
            # Not starting with a dot
            if [[ "${element}" != .* ]]; then
                # Only sort if not starting with a 0
                if [[ "${element}" != 0* ]]; then
                    # Sort the directory
                    torrent-sort "${element}"
                fi
            fi
        fi
    done
}

# - TREATMENT

# Treat all directories and files of the current directory
function torrent-process() {
    # Go to the ToSort directory
    cd "${TOSORT_PATH}"
    # Unpack then pack elements of the current directory
    torrent-unpack-pack
    # Sort all directories of the current directory
    torrent-sort-dirs
}