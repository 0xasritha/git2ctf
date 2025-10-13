# TODO: pass in arg, and then execute that specific function, so can break up visually in Github Actions 

"""

PR Check Github Actions should: 
    - go through the commited files and get all the changed ones 
    - for each directory /challenges/<category>/<challenge-name> that contains some files that have been changed, call this script with the appropriate path variables provided 
"""


import os 
import sys 
import yaml 

USED_PORTS = os.getenv("USED_PORTS") or sys.exit("USED_PORTS is not set")
CHALLENGE_PATH = os.getenv("CHALLENGE_PATH") or sys.exit("CHALLENGE_PATH is not set")
    # serialize 
    # make sure this would not break if it is empty 
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE") or sys.exit("GITHUB_WORKSPACE is not set")

#TODO: rename these all to be consistent 

#TODO: apparently ur supposed to use pathlib? 
info_yaml_path = os.path.join(GITHUB_WORKSPACE + "/challenges/" + CHALLENGE_PATH)

with open(info_yaml_path) as f: 
    challenge_config = yaml.safe_load(f)

def unique_port(): 
    # get current port (use that docker thing)
    return False  

def compose_file_named_correctly(): 
# make sure all variations of "docker-compose.yaml" are named "compose.yaml"
    return False 

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
