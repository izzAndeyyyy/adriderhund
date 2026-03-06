import yaml
from netmiko import ConnectHandler
from datetime import datetime
import os

backup_dir = "configs"

with open("devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

for device in devices:

    try:

        connection = ConnectHandler(
            device_type=device["type"],
            host=device["ip"],
            username="backup",
            password="backup123"
        )

        config = connection.send_command("show running-config")

        filename = f"{backup_dir}/{device['name']}_{datetime.now().date()}.cfg"

        with open(filename, "w") as file:
            file.write(config)

        connection.disconnect()

        print(f"{device['name']} backup successful")

    except Exception as e:

        print(f"{device['name']} backup failed")

os.system("git add .")
os.system('git commit -m "daily config backup"')

os.system("aws s3 sync configs s3://backup-bucket-cloud")
