#!/bin/bash

SOFTWARE_DIR="$PWD"
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
ExecStart=/usr/bin/python3 $SOFTWARE_DIR/fan_control_script.py --no_console_log_stream
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

if ! grep -q "alias fan-control-logs=" ~/.bashrc; then
    echo "alias fan-control-logs='tail -f -n 15 $SOFTWARE_DIR/fan_control.log'" >> ~/.bashrc
    echo "Command 'fan-control-logs' added to view logs."
    echo "Please source ~/.bashrc manually for the fan-control-logs alias to become effective immediately."
else
    echo "Alias 'fan-control-logs' already exists in ~/.bashrc."
fi