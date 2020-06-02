#!/bin/bash

DIR=$(dirname "$0")
CWD=$(readlink -m $DIR)

echo "Creating environment file..."
mkdir -p /etc/dubois  
echo "DUBOIS_DIR=$CWD" > /etc/dubois/dubois.conf

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
echo "Done! Please run 'sudo reboot' to reboot your device."
