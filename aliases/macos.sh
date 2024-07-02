#!/bin/bash
# Aliases for MacOS.
# Created by LounisBou

# ----------------------------------
# ! Mac OS 
#
# READ THIS CAREFULLY BEFORE USING THIS FILE:
# 
# Commands in this section are work in progress.
# They are not ready to be used.
# Please do not use them.
#

# GLOBAL VARIABLES

# COMMANDS

# Check if system type is macos
if [[ $(uname) == "Darwin" ]]; then

  # ----------------------------------
  # ! Close Apps
  function close-apps(){
    # Close all apps
    osascript -e 'tell application "System Events" to set quitapps to name of every application process whose visible is true and name is not "Finder" and name is not "iTerm2" and name is not "Terminal"'
    for app in $quitapps; do
      osascript -e "tell application \"$app\" to quit"
    done
  }

  # ----------------------------------
  # ! Mac OS Launch Daemon User Services

  # Load Launch Daemon User Service
  function services-load(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Load service
    launchctl load -w $HOME/Library/LaunchAgents/$1
  }
  # Load Launch Daemon User Service auto-completion
  function _services-load(){
    _files -W $HOME/Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-load services-load

  # Unload Launch Daemon User Service
  function services-unload(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Unload service
    launchctl unload -w $HOME/Library/LaunchAgents/$1
  }
  # Unload Launch Daemon User Service auto-completion
  function _services-unload(){
    _files -W $HOME/Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-unload services-unload

  # Restart Launch Daemon User Service
  function services-reload(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Unload/Load service
    launchctl unload -w $HOME/Library/LaunchAgents/$1
    launchctl load -w $HOME/Library/LaunchAgents/$1
  }
  # Restart Launch Daemon User Service auto-completion
  function _services-reload(){
    _files -W $HOME/Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-reload services-reload

  # List Launch Daemon User Services
  function services-list(){
    # List services
    launchctl list | grep -v com.apple
  }

  # Check Launch Daemon User Service Status
  function services-status(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Check service status
    launchctl list | grep $1
  }
  # Check Launch Daemon User Service Status auto-completion
  function _services-status(){
    _files -W $HOME/Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-status services-status

  # Check Launch Daemon User Service File Syntax
  function services-syntax(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Check service file syntax
    launchctl print $1
  }
  # Check Launch Daemon User Service File Syntax auto-completion
  function _services-syntax(){
    _files -W $HOME/Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-syntax services-syntax

  # ----------------------------------
  # ! Mac OS Launch Daemon Global Services

  # Load Launch Daemon Global Service
  function services-global-load(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Load service
    launchctl load -w /Library/LaunchAgents/$1
  }
  # Load Launch Daemon Global Service auto-completion
  function _services-global-load(){
    _files -W /Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-global-load services-global-load

  # Unload Launch Daemon Global Service
  function services-global-unload(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Unload service
    launchctl unload -w /Library/LaunchAgents/$1
  }
  # Unload Launch Daemon Global Service auto-completion
  function _services-global-unload(){
    _files -W /Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-global-unload services-global-unload

  # Restart Launch Daemon Global Service
  function services-global-reload(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Unload/Load service
    launchctl unload -w /Library/LaunchAgents/$1
    launchctl load -w /Library/LaunchAgents/$1
  }
  # Restart Launch Daemon Global Service auto-completion
  function _services-global-reload(){
    _files -W /Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-global-reload services-global-reload

  # List Launch Daemon Global Services
  function services-global-list(){
    # List services
    launchctl list | grep com.apple
  }

  # Check Launch Daemon Global Service Status
  function services-global-status(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Check service status
    launchctl list | grep $1
  }
  # Check Launch Daemon Global Service Status auto-completion
  function _services-global-status(){
    _files -W /Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-global-status services-global-status

  # Check Launch Daemon Global Service File Syntax
  function services-global-syntax(){
    # Check if service name is empty
    if [ -z "$1" ]; then
      echo "Service name is required."
      return
    fi
    # Check service file syntax
    launchctl print $1
  }
  # Check Launch Daemon Global Service File Syntax auto-completion
  function _services-global-syntax(){
    _files -W /Library/LaunchAgents/ -g '*.plist' -/
  }
  compdef _services-global-syntax services-global-syntax

  # ----------------------------------
  # ! Open in Apps

  # Open in Finder
  alias open-finder="open -a Finder $*"

  # Open in VSCode
  alias open-vscode="open -a /Applications/Visual\ Studio\ Code.app $*"

  # Open in Sublime Text
  alias open-sublime="open -a /Applications/Sublime\ Text.app $*"

  # Open in PyCharm
  alias open-py="open -a /Applications/PyCharm.app $*"

  # Open in PhpStorm
  alias open-php="open -a /Applications/PhpStorm.app $*"

  # Open in Android Studio
  alias open-android="open -a /Applications/Android\ Studio.app $*"

  # Open in Xcode
  alias open-xcode="open -a /Applications/Xcode.app $*"

  # Open in Chrome
  alias open-chrome="open -a /Applications/Google\ Chrome.app $*"

  # Open in Firefox
  alias open-firefox="open -a /Applications/Firefox.app $*"

  # Open in Safari
  alias open-safari="open -a /Applications/Safari.app $*"

  # Open in VLC
  alias open-vlc="open -a /Applications/VLC.app $*"

  # ----------------------------------
  # ! Mkcert

  # mkcert : generate local ssl certificates
  alias sslcert="mkcert -install && mkcert localhost $*"

  # Create certificate for homebrew httpd vhost
  function httpd-cert-vhost(){
    # Create variable vhost
    vhost=$1
    # Check if vhost is empty
    if [ -z "$vhost" ]; then
      # Retrieve vhosts files list
      vhostsFiles=(/opt/homebrew/etc/httpd/extra/sites-enabled/*)
      # Echo vhosts list
      echo "List of available vhosts:"
      # Create a list of vhosts
      vhosts=()
      # Loop through vhosts files
      for filepath in $vhostsFiles; do
        # Retrieve filename
        filename=$(basename "$filepath")
        # Retrieve vhost name and add it to vhosts list
        vhosts+=$(echo "$filename" | sed 's/\.conf//')
      done
      select selected_vhost in "${vhosts[@]}"; do
        if [ -n "$selected_vhost" ]; then
          vhost="$selected_vhost"
          break
        else
          echo "Invalid selection. Please try again."
        fi
      done
      # Print vhost name
      echo "Vhost name: $vhost"
    fi

    # Vhost file path
    vhostFilepath="/opt/homebrew/etc/httpd/extra/sites-enabled/$vhost.conf"
    # Check if vhost file exists
    if [ ! -f "$vhostFilepath" ]; then
      echo "Vhost file not found : $vhostFilepath"
      return
    fi
    
    # Read vhosh file content
    content=$(cat "/opt/homebrew/etc/httpd/extra/sites-enabled/$vhost.conf")
    # Retrieve domain file contains : define SITE "api.domain.local"
    domain=$(echo "$content" | grep "define SITE" | sed 's/define SITE "//' | sed 's/"//')
    # Echo domain
    echo "Certificat will be create for : $domain"
    # Ask user if he wants to add more domains
    read REPLY"?Add more domains ? (y/n) "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      # Ask user to enter domains
      read domains"?Enter domains (separated by space): " 
    else 
      # Add domain to domains list
      domains=""
    fi

    # SSL directory path
    sslDir="/opt/homebrew/etc/httpd/ssl/$vhost"

    # mkcert command
    command="mkcert -install && mkcert --key-file cert.key --cert-file cert.crt $domain $domains localhost 127.0.0.1 ::1"

    # Create certificate
    echo "Command : $command"

    # Ask user for confirmation
    read REPLY"?Create certificate ? (y/n) "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      # Check if ssl directory exists
      if [ ! -d "$sslDir" ]; then
        # Create ssl directory
        mkdir "$sslDir"
      fi
      # Go to ssl directory
      cd "$sslDir"
      # Execute command
      eval $command
      # Go back to previous directory
      cd -
      # Print generated files
      ls -la "$sslDir"
    else
      echo "Certificate creation aborted."
    fi
  }

  # ----------------------------------
  # ! TOR Proxy

  # Activation du proxy tor
  function torStart(){ 
    # Configuration du port d'écoute du proxy MAC.
    networksetup -setsocksfirewallproxy Wi-Fi localhost $TOR_SOCKS_PORT
    # Mac proxy activation.
    networksetup -setsocksfirewallproxystate Wi-Fi on && echo "Configuration proxy du MAC activée."
    # Activation du service tor.
    brew services start tor
  }

  # Désactivation du proxy tor
  function torStop(){ 
    # Mac proxy désactivation.
    networksetup -setsocksfirewallproxystate Wi-Fi off && echo "Configuration proxy du MAC désactivée."
    # Désactivation du service tor.
    brew services stop tor
  }

  # Activation du proxy tor
  function torRestart(){ 
    # Tor Stop && Tor Start.
    torStop && torStart && echo 'Restart done.'
  }

  # Chose TOR Exit Node
  function torCheck(){ 
    # Show TOR config values.
    cat /etc/torrc.exit
  }

  # Chose TOR Entry Node
  function torIn(){ 
    # Modify TOR Entry Node with arg value.
    echo "EntryNodes {$1} StrictNodes 1" > /opt/homebrew/etc/tor/torrc.entry
    # Restart TOR.
    torRestart
  }

  # Chose TOR Exit Node
  function torOut(){ 
    # Modify TOR Exit Node with arg value.
    echo "ExitNodes {$1} StrictNodes 1" > /opt/homebrew/etc/tor/torrc.exit
    # Restart TOR.
    torRestart
  }

fi