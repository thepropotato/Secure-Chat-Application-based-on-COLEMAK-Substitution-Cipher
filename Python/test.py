import hashlib
import platform
import os
import socket
import uuid
import json

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(2,7)][::-1])
    return mac

def get_os_info():
    return platform.system() + " " + platform.version()

def get_hardware_info():
    return platform.machine()

def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return {"hostname": hostname, "ip_address": ip_address}

def generate_device_fingerprint():
    # Check if the UUID is already generated and stored
    if os.path.exists("device_uuid.txt"):
        with open("device_uuid.txt", "r") as file:
            uuid_str = file.read().strip()
    else:
        # Generate a new UUID and store it
        uuid_str = str(uuid.uuid4())
        with open("device_uuid.txt", "w") as file:
            file.write(uuid_str)

    fingerprint_data = {
        "MAC add" : get_mac_address(),
        "os_info": get_os_info(),
        "hardware_info": get_hardware_info(),
        "network_info": get_network_info(),
        "uuid": uuid_str
    }

    # Convert the fingerprint data to a JSON string
    fingerprint_json = json.dumps(fingerprint_data, sort_keys=True)

    # Hash the JSON string to create a unique fingerprint
    fingerprint_hash = hashlib.md5(fingerprint_json.encode()).hexdigest()

    return fingerprint_hash