import socket
import subprocess
import os

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port: int = 8080, max_port: int = 8099) -> int:
    for port in range(start_port, max_port + 1):
        if not is_port_in_use(port):
            return port
    raise RuntimeError(f"No available ports between {start_port} and {max_port}")

def start_server(app_dir: str, port: int):
    """
    Start python's built-in http.server in the background.
    """
    # Create the directory if it doesn't exist
    os.makedirs(app_dir, exist_ok=True)
    
    # Use subprocess.Popen to start it in the background
    process = subprocess.Popen(
        ["python", "-m", "http.server", str(port)],
        cwd=app_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return process.pid

def ensure_server_running(app_name: str, start_port: int = 8080) -> int:
    """
    Check if a server for this app is already running by checking some state file,
    or just start a new one if it's the first time.
    For Phase 1, we can just find a port and start it.
    If we want to reuse ports for the same app, we'd need to store the mapping.
    For simplicity, let's store mapping in a local json file.
    """
    import json
    mapping_file = os.path.join(os.path.dirname(__file__), "port_mapping.json")
    mapping = {}
    
    if os.path.exists(mapping_file):
        try:
            with open(mapping_file, "r") as f:
                mapping = json.load(f)
        except Exception:
            pass
            
    if app_name in mapping:
        port = mapping[app_name]["port"]
        if is_port_in_use(port):
            return port
            
    # Port is not in use, so we need to allocate and start
    port = find_available_port(start_port)
    app_dir = os.path.join(os.path.dirname(__file__), "apps", app_name)
    start_server(app_dir, port)
    
    mapping[app_name] = {"port": port}
    with open(mapping_file, "w") as f:
        json.dump(mapping, f)
        
    return port
