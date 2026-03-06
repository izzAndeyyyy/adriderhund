import subprocess
import yaml
import re

# Management VLAN
network = "10.1.40.0/24"

print("Scanning management VLAN...")

scan = subprocess.check_output([
    "nmap",
    "-p", "22",
    "--open",
    network
]).decode()

ips = re.findall(r"Nmap scan report for (\d+\.\d+\.\d+\.\d+)", scan)

devices = []

for ip in ips:

    name = f"device-{ip.replace('.', '-')}"
    dev_type = "mikrotik_ios"

    devices.append({
        "name": name,
        "ip": ip,
        "type": dev_type
    })

data = {"devices": devices}

with open("devices.yaml", "w") as f:
    yaml.dump(data, f)

print("Discovery finished")
