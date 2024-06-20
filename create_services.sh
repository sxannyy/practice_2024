#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: Missing parameters."
    echo "Usage: $0 <date>"
    exit 1
fi

FILES_DIR="./data/$1"
SYSTEMD_DIR="/etc/systemd/system"

if [ ! -d "$FILES_DIR" ]; then
    echo "Error: Directory $FILES_DIR does not exist."
    exit 1
fi

for file in "$FILES_DIR"/*; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file")
        service_name="publisher@$1--$filename"
        echo $service_name

        if systemctl list-unit-files | grep -q "$service_name.service"; then
            echo "Warning: Service $service_name already exists. Skipping."
            continue
        fi

        echo "Creating service file for $file"
        sudo bash -c "cat > $SYSTEMD_DIR/$service_name.service <<EOL
[Unit]
Description=Publisher Service for $filename

[Service]
ExecStart=/usr/bin/python3 /home/ivan/Рабочий\ стол/open-source/praktika/publisher.py $1 $filename
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL"

        if [ $? -ne 0 ]; then
            echo "Error: Failed to create service file for $file"
            continue
        fi

        echo "Reloading systemd daemon"
        sudo systemctl daemon-reload
        if [ $? -ne 0 ]; then
            echo "Error: Failed to reload systemd daemon"
            continue
        fi

        echo "Enabling service $service_name"
        sudo systemctl enable "$service_name.service"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to enable service $service_name"
            continue
        fi

        echo "Starting service $service_name"
        sudo systemctl start "$service_name.service"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to start service $service_name"
            continue
        fi
    fi
done
