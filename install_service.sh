#!/bin/bash

DIR=$(dirname "$0")
CWD=$(readlink -m $DIR)

echo "Creating environment file..."
mkdir -p /etc/dubois  
echo "DUBOIS_DIR=$CWD" > /etc/dubois/dubois.conf

echo "Copying dubois.sh to bin folder..."
cp $CWD/dubois.sh /usr/bin/dubois.sh
echo "Granting permissions to daemon..."
chmod +x /usr/bin/dubois.sh
echo "Copying service to systemd folder..."
cp $CWD/dubois/dubois.service /etc/systemd/system/dubois.service
echo "Granting permission to service..."
chmod 644 /etc/systemd/system/dubois.service
echo "Enabling service..."
systemctl enable dubois
echo "Done! Please run 'sudo reboot' to reboot your device."
