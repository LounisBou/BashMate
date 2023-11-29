# Title: DomMate
# Language: Bourne Again Shell
# Creator: LounisBou
# Access: Public
# Category: System
# Type: Configuration
# Tags: Domotic, Openhab, Zigbee2mqtt, Mosquitto, MQTT, Zigbee, Zwave
#
# Description: 
#
# Usage:
# Source this file in your .bashrc or .zshrc file.
#
#
# Get absolute directory of the current file.
currentDir="$(realpath $(dirname "$0"))"
#
#
# Check if system type is macos
if [[ $(uname) == "Darwin" ]]; then
    echo "Macos based system detected"
    OS_TYPE="macos"
# Check if system type is debian based
elif [[ "$(expr substr $(uname -s) 1 5)" == "Linux" ]]; then
    echo "Linux based system detected"
    OS_TYPE="linux"
# Check if system type is windows
elif [[ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]]; then
    echo "Windows based system detected"
    OS_TYPE="windows"
fi

# ! Install mosquitto

# Check OS type
if [[ "$OS_TYPE" == "macos" ]]; then
    # Check if mosquitto is installed
    if brew ls --versions mosquitto > /dev/null; then
        # The package is installed
        echo "Mosquitto is already installed"
    else
        # The package is not installed
        echo "Installing Mosquitto..."
        # Install mosquitto
        brew install mosquitto
        brew install mosquitto-clients
        # Start mosquitto
        brew services start mosquitto
    fi
elif [[ "$OS_TYPE" == "linux" ]]; then
    # Check if mosquitto is installed
    if dpkg -s mosquitto > /dev/null; then
        # The package is installed
        echo "Mosquitto is already installed"
    else
        # The package is not installed
        echo "Installing Mosquitto..."
        # Install mosquitto
        sudo apt-get install mosquitto
        sudo apt-get install mosquitto-clients
        # Start mosquitto
        sudo systemctl start mosquitto
    fi
fi


# ! Install zigbee2mqtt

# Check if nodejs is installed
if [[ "$OS_TYPE" == "macos" ]]; then
    # Check if nodejs is installed
    if brew ls --versions node > /dev/null; then
        # The package is installed
        echo "Nodejs is already installed"
    else
        # The package is not installed
        echo "Installing Nodejs..."
        # Install nodejs
        brew install node
    fi
elif [[ "$OS_TYPE" == "linux" ]]; then
    # Check if nodejs is installed
    if dpkg -s node > /dev/null; then
        # The package is installed
        echo "Nodejs is already installed"
    else
        # The package is not installed
        echo "Installing Nodejs..."
        # Install nodejs
        # Set up Node.js repository and install Node.js + required dependencies
        # NOTE 1: Older i386 hardware can work with [unofficial-builds.nodejs.org]
        #   (https://unofficial-builds.nodejs.org/download/release/v16.15.0/ e.g. 
        #   Version 16.15.0 should work.
        # NOTE 2: For Ubuntu see tip below
        sudo curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
        sudo apt-get install -y nodejs git make g++ gcc
        # Verify that the correct nodejs and npm (automatically installed with nodejs)
        # version has been installed
        node --version  # Should output V16.x, V17.x, V18.X or V20.X
        npm --version  # Should output 6.X, 7.X or 8.X
    fi
fi

# The package is not installed
echo "Installing Zigbee2mqtt..."
# Install zigbee2mqtt
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
sudo chown -R ${USER}: /opt/zigbee2mqtt
# Install zigbee2mqtt dependencies
npm install --prefix /opt/zigbee2mqtt
# Build the app
npm run build --prefix /opt/zigbee2mqtt
# Retrieve zigbee2mqtt configuration from github repository
git clone $ZIGBEE2MQTT_CONFIG_REPO /opt/zigbee2mqtt/data-backup
# Check if configuration.yaml file exists
if [ -f /opt/zigbee2mqtt/data-backup/configuration.yaml ]; then
    # Save current configuration
    mv /opt/zigbee2mqtt/data/configuration.yaml /opt/zigbee2mqtt/data/configuration.yaml.bak
fi
# Link data-backup/configuration.yaml to data/configuration.yaml
ln -s /opt/zigbee2mqtt/data-backup/configuration.yaml /opt/zigbee2mqtt/data/configuration.yaml
# Create log files
touch /opt/zigbee2mqtt/data/log-stderr.txt
touch /opt/zigbee2mqtt/data/log-stdout.txt
# Change log files owner to root
sudo chown root /opt/zigbee2mqtt/data/log-stderr.txt
sudo chown root /opt/zigbee2mqtt/data/log-stdout.txt
# Change log files permissions
sudo chmod 777 /opt/zigbee2mqtt/data/log-stderr.txt
sudo chmod 777 /opt/zigbee2mqtt/data/log-stdout.txt
# Create zigbee2mqtt service
if [[ "$OS_TYPE" == "macos" ][]; then
    # Copy zigbee2mqtt plist file
    sudo cp $currentDir/includes/zigbee2mqtt.plist /Library/LaunchDaemons/zigbe2mqtt.plist
    # Load zigbee2mqtt service
    sudo launchctl load /Library/LaunchDaemons/zigbe2mqtt.plist
    # Start zigbee2mqtt service
    sudo launchctl start zigbe2mqtt
elif [[ "$OS_TYPE" == "linux" ]]; then
    # Copy zigbee2mqtt service file
    sudo cp $currentDir/includes/zigbee2mqtt.service /etc/systemd/system/zigbee2mqtt.service
    # Reload systemd
    sudo systemctl daemon-reload
    # Enable zigbee2mqtt service
    sudo systemctl enable zigbee2mqtt.service
    # Start zigbee2mqtt service
    sudo systemctl start zigbee2mqtt
    # View the log of Zigbee2MQTT service
    sudo journalctl -u zigbee2mqtt.service -f
fi


# ! Install openhab

# Check OS type
if [[ "$OS_TYPE" == "macos" ]]; then
    # Check if openhab is installed
    if brew ls --versions openhab > /dev/null; then
        # The package is installed
        echo "Openhab is already installed"
    else
        # The package is not installed
        echo "Installing Openhab..."
        # Install openhab
        brew install openhab
        brew install openhab-cli
        # Start openhab
        brew services start openhab
    fi
elif [[ "$OS_TYPE" == "linux" ]]; then
    # Check if openhab is installed
    if dpkg -s openhab > /dev/null; then
        # The package is installed
        echo "Openhab is already installed"
    else
        # The package is not installed
        echo "Installing Openhab..."
        # Install openhab
        sudo apt-get install openhab
        sudo apt-get install openhab-cli
        # Start openhab
        sudo systemctl start openhab
    fi
fi

