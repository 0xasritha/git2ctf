# pylint: skip-file 
#TODO: get rid of ^ 
# TODO: pass in arg, and then execute that specific function, so can break up visually in Github Actions 

import os 
import sys 
import yaml 
from pathlib import Path
import subprocess 
import json 


USED_PORTS = os.getenv("USED_PORTS") or sys.exit("USED_PORTS is not set")
CHALLENGE_PATH = os.getenv("CHALLENGE_PATH") or sys.exit("CHALLENGE_PATH is not set")
    # serialize 
    # make sure this would not break if it is empty 
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE") or sys.exit("GITHUB_WORKSPACE is not set")

#TODO: rename these all to be consistent 

#TODO: apparently ur supposed to use pathlib? 
info_yaml_path = os.path.join(GITHUB_WORKSPACE, "/challenges/", CHALLENGE_PATH)

full_challenge_dir_path = os.path.join(GITHUB_WORKSPACE, CHALLENGE_PATH)

#TODO: set error string?  -> how to return output? 
USED_PORTS = [8080, 8081, 3000]  # example global list


with open(info_yaml_path) as f: 
    challenge_config = yaml.safe_load(f)

def unique_port():
    """
    Check if all ports defined in compose.yaml are unique
    (i.e., not in USED_PORTS). Returns True if safe to use.
    """
    if not compose_file_named_correctly():
        print("Compose file named incorrectly.")
        return False

    chall_dir = Path(os.getenv("GITHUB_WORKSPACE", ".")) / os.getenv("CHALLENGE_PATH", "")
    compose_file = chall_dir / "compose.yaml"

    if not compose_file.is_file():
        print("No compose.yaml found.")
        return False

    # Run docker compose config and extract ports
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "config", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running docker compose config: {e}")
        return False

    try:
        compose_config = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Invalid JSON output from docker compose config.")
        return False

    used_in_compose = set()

    for service in compose_config.get("services", {}).values():
        for port_entry in service.get("ports", []):
            if isinstance(port_entry, dict):
                published = port_entry.get("published")
                if published:
                    used_in_compose.add(int(published))

    if not used_in_compose:
        print("No published ports found in compose.yaml.")
        return True

    conflicts = used_in_compose.intersection(USED_PORTS)
    if conflicts:
        print(f"Conflict found — ports already used: {sorted(conflicts)}")
        return False

    print(f"Ports {sorted(used_in_compose)} are unique.")
    return True


def compose_file_named_correctly(): 
   bad_names = [
        "docker-compose.yaml",
        "docker-compose.yml",
        "compose.yml",
    ]
   for name in bad_names:
        if os.path.isfile(os.path.join(full_challenge_dir_path, name)):
            return False
   return True

# also check for no random fields added 
def required_fields(): 
    return False 

def flag_format_is_correct():
    challenge_config["flag"]
    return False 

def correct_yaml_formatting(): 
    return False 

def check_connection_string():
    return False # check that it is not specified boofly 
    # connection info field not always required 

def zip_static_assets(): # must be zipped the same way  
    return False 


CHECKS = { 

}

if len(sys.argv) != 1: 
    print("Error: No check provided.\n")
    sys.exit(1)

check = sys.argv[1]
check_func = CHECKS.get(check) 
if check_func is None: 
    print(f"Error: Unknown command '{check}'.\n")
    sys.exit(1)

check_func() # based on if check_func() passes, the github action should fail or succeed, but should run all checks and fail if atleast one of the checks fail 
