import os
import sys

def create_service_file(date, filename):
    service_name = f"publisher_{date}_{filename}.service"
    service_content = f"""
[Unit]
Description=Publisher service file {filename} for date {date}
After=network.target

[Service]
Type=simple
ExecStart=/bin/python /home/ivan/praktika/publisher.py {date} {filename}
Restart=on-failure

[Install]
WantedBy=default.target
"""

    service_dir = "/etc/systemd/system/"
    service_path = os.path.join(service_dir, service_name)

    try:
        with open(service_path, "w") as service_file:
            service_file.write(service_content)
        print(f"Created service file: {service_path}")
        return service_name
    except PermissionError:
        print(f"Permission denied: {service_path}")
        return
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: create_services.py <date>")
        sys.exit(1)

    date = sys.argv[1]
    folder_path = os.path.join("data", date)

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        sys.exit(1)
    
    service_files = []
    for filename in os.listdir(folder_path):
        print(service_files)
        if filename.endswith(".rnx"):
            file_base = os.path.splitext(filename)[0]
            service_file = create_service_file(date, file_base)
            if service_file:
                service_files.append(service_file)

    print("Reloading systemd manager configuration...")
    os.system("sudo systemctl daemon-reload")

    for service in service_files:
        print(f"Enabling and starting service: {service}")
        os.system(f"sudo systemctl enable --now {service}")
