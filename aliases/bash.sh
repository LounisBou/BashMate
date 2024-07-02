# Aliases for bourne again shell.
# Created by LounisBou

# GLOBAL VARIABLES

# COMMANDS

# Restart bash 
alias rebash="source ~/.bashrc"
# Restart zsh
alias rezsh="source ~/.zshrc"

# Shutdown and reboot
alias shutdown="sudo shutdown -h now"
alias reboot="sudo reboot"

# List all files with permissions
alias ll="ls -al"
# List all files with permissions in tree mode
alias llt="tree -u -g -D -p"
# Get the real path of a file
alias path="realpath $*" 
# Clear terminal
alias cl="clear"
# Watch aliases
function watcha(){
  # Show execution result of command
  watch -x zsh -ic "$*"
}

# ! INTERACTIVE PROMPT COMMANDS

# Interactive prompt prefix commands
function interactive-prompt(){
    # Use fzf to select prefix* commands, order them by name
    local command=$(compgen -A function | grep "${$0}[^=]\+" | sort | fzf)
    # Check if the command is not empty
    if [ -n "$command" ]; then
        if [[ -n $ZLE_LINE_TEXT ]]; then
            # When zle is active (e.g., via key binding)
            BUFFER="$command "
            CURSOR=${#BUFFER}
            zle -R -c
        else
            # When zle is not active (e.g., direct invocation)
            print -z "$command "
        fi
    fi
}
# /!\ Dont forget to call : 
#zle -N prefix

# ! SYSTEM USER 

# Add group to user (add-group <groupname> <username>)
alias add-group="sudo usermod -a -G"

# ! FILESYSTEM 

# Create folder for each file
function folderPack(){
  for x in ./*.*; do
    mkdir "${x%.*}" && mv "$x" "${x%.*}"
  done
}

# Rename
function rname(){
	cmd="rename 's/$1/$2/g' *"
	echo $cmd
	eval $cmd
}

# ! NMAP.

# Check all machines on LAN.
function onLan(){ 
  nmap -sPn $1/24
}

# Check for specific port on LAN.
function onLanPort(){ 
  nmap -sS $1/24 -p $2
}

# Check all machines on LAN.
function onLanDevices(){ 
  nmap -sn $1/24
}

# Get info on specific machine on LAN.
function onLanDevice(){ 
  sudo nmap -O $1
}

# Get info on specific machine on LAN.
function onLanDevicePlus(){ 
  sudo nmap -A $1
}

# ! TAR/UNTAR (Compression/Décompression) :

# targz : Compress folder in tar.gz file.
function targz(){ 
	tar -pcvzf $1.tar.gz $1
}

# untargz : Uncompress tar.gz file in current folder.
function untargz(){ 
	tar -zxvf $1
}

# Local IP address
alias ip="ipconfig getifaddr en0"
# External IP V4 address 
alias IP="curl -4 icanhazip.com"
# External IP V6 address 
alias IP6="curl -6 icanhazip.com"

# ! NETWORK

# Check if a remote port is open
function net-port-check(){
  # Check if the host argument is empty
  if [ -z $1 ]; then
    echo "${YELLOW}Please provide a IP or host name.${NC}"
    return 1
  fi
  # Check if the port argument is empty
  if [ -z $2 ]; then
    echo "${YELLOW}Please provide a port number.${NC}"
    return 1
  fi
  # Check if the remote port is open
  if nc -z $1 $2; then
    echo "${GREEN}Port $2 is open on $1${NC}"
  else
    echo "${RED}Port $2 is closed on $1${NC}"
  fi
}

# Wait while a remote port is open
function net-port-wait(){
  # Check if the host argument is empty
  if [ -z $1 ]; then
    echo "${YELLOW}Please provide a IP or host name.${NC}"
    return 1
  fi
  # Check if the port argument is empty
  if [ -z $2 ]; then
    echo "${YELLOW}Please provide a port number.${NC}"
    return 1
  fi
  # Wait while the remote port is open
  while ! nc -z $1 $2; do
    echo "${YELLOW}Waiting for port $2 to open on $1${NC}"
    sleep 1
  done
  echo "${GREEN}Port $2 is open on $1${NC}"
}

