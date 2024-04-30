#!/bin/bash

SYSTEMD_SERVICE="/etc/systemd/system/fan-control.service"

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

# Check if the service is running
if systemctl is-active --quiet fan-control; then
    echo "The fan-control service is already running."
else
    # Start the service
    if systemctl start fan-control; then
        echo "The fan-control service has been started successfully."
    else
        echo "Error: Unable to start the fan-control service."
    fi
fi
