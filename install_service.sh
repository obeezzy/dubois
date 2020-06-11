#!/bin/bash

DIR=$(dirname "$0")
CWD=$(readlink -m $DIR)

echo "Creating environment file..."
mkdir -p /etc/dubois  
echo "DUBOIS_DIR=$CWD" > /etc/dubois/dubois.conf
cat >> /etc/dubois/dubois.conf << EOF
# Uncomment to specify log level. Valid values are debug, info, warning and critical.
# LOGLEVEL=warning

###################### Environment ############################
# All pin numbers specified are Broadcom (BCM).

# Maps buzzer pin
# BUZZER_PIN=26

# Maps RGB indicator pin
# INDICATOR_PINS=14,16,15

# Maps headlights pin
# HEADLIGHTS_PIN=7

# Maps left wheel pins
# LEFT_WHEEL_PINS=18,23

# Maps right wheel pins
# RIGHT_WHEEL_PINS=24,25

# Maps left wheel enable pin
# LEFT_WHEEL_ENABLE_PIN=5

# Maps right wheel enable pin
# RIGHT_WHEEL_ENABLE_PIN=6
EOF

echo "Copying start_dubois.sh to bin folder as dubois.sh..."
cp $CWD/start_dubois.sh /usr/bin/dubois.sh
echo "Granting permissions to daemon..."
chmod +x /usr/bin/dubois.sh
echo "Copying service to systemd folder..."
cp $CWD/dubois/service/dubois.service /etc/systemd/system/dubois.service
echo "Granting permission to service..."
chmod 644 /etc/systemd/system/dubois.service
echo "Enabling service..."
systemctl enable dubois
echo "Done!"
echo "Run 'sudo reboot' to reboot your device."
