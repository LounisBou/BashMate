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