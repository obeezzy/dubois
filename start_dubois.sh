#!/bin/bash

if [[ -z "$DUBOIS_DIR" ]]; then
    echo "DUBOIS_DIR not set. Trying running the 'setup.sh' script in your dubois folder."
    exit 1
fi

DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Dubois service started at ${DATE}." | systemd-cat -p info

export PYTHONPATH=$DUBOIS_DIR
$DUBOIS_DIR/dubois/service/duboisd.py
