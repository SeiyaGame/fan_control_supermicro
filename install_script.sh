#!/bin/bash

SOFTWARE_DIR="/opt/fan_control_supermicro"
GIT_REPO="https://github.com/SeiyaGame/fan_control_supermicro.git"
SYSTEMD_SERVICE="/etc/systemd/system/fan-control.service"

if [[ -d "$SOFTWARE_DIR" ]]; then
    echo "Script already installed, attempt to update !"
    cd $SOFTWARE_DIR && git pull origin main
else
    echo "Cloning the repository..."
    git clone $GIT_REPO $SOFTWARE_DIR
fi

if [[ ! -e "$SYSTEMD_SERVICE" ]]; then

    echo "Installation of the service in progress ..."

cat <<EOF > /etc/systemd/system/fan-control.service
[Unit]
Description=Fan Control Service
After=network-online.target

[Service]
Type=simple
ExecStartPre=/usr/bin/sleep 10
ExecStart=/usr/bin/python3 $SOFTWARE_DIR/fan_control_script.py
WorkingDirectory=$SOFTWARE_DIR
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    echo "The service has been successfully installed !"
else
    echo "Service already installed !"
fi
