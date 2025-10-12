# parse YAML file  

# checks if UUID already exists in the map, quit 

# if not, will proceed to create challenge 

# update connection info template string 

# build request with all defaults 

# send request to CTFd 

#TODO: feed this into chat at the end and tell it to clean up any bad variable names 
import sys 
import yaml 
import requests 

CTFD_URL = "http://localhost:8000"
parent_folder_name = "web" #TODO: need to make this pulled from the path 
CTFD_TOKEN = "ctfd_4ada4094eb01ab7e37aba83c077b68d900f5ce2d4649df7ee111cb16d8f0f7fa"

# uuid : ctfd-id
existing_challenges = {
    "1d5d7c44-120a-4d18-b3e3-f44125630e7a": 9
}

# some values could have None if just (flag: )
# standardize all format somehow ? YAML standardizer?  
with open('./sample.yaml') as f: 
    challenge_config = yaml.safe_load(f)

# print(challenge_config)

if existing_challenges.get(challenge_config["uuid"]):
    print("Challenge already exists!")
    sys.exit() # combine with the update-challenge script 

# parent-folder-name : category on CTFd 
categories = { 
    "web": "Web Exploitation" , 
    "misc": "Miscellaneous", 
    "pwn": "Binary Exploitation",   
    "rev": "Reverse Engineering", 
    "crypto": "Cryptography", 
    "forensics": "Forensics", 
    "hardware": "Hardware", 
    "rf": "RF (Radio Frequencies)", 
    "osint": "OSINT", 
}
session = requests.Session()
session.headers.update({"Authorization": f"Token {CTFD_TOKEN}"})

"""

display-name-on-ctfd: "Reversing Challenge"
uuid: "8dbe4bf4-d57d-403c-8ad5-0a283162d2cd"
flag: "MINUTEMAN{XXXX}"
description: "asdfasdf" # have example showing newlines in YAML
connection-info: "{{ HOST }}:{{ PORT }}"
attribution: "asritha bodepudi" # change this to author name?
tags:
  - web
  - sandbox
  - js
hints:
  - "This is first hint"
  - "This is the second hint"
# category: must change folder

"""
# say something in docs -> if you have multiple flags or some other niche thing, reach out to us for custom deployment. then give examples of other niche things that CTFd supports 

create_challenge_payload = {
    "name": challenge_config["display-name-on-ctfd"],  
    "category": categories[parent_folder_name], 
    "description": challenge_config["description"], 
    "state": "hidden",  # TODO: will we make this public just in the CTFd console? 
    "initial":"100",
    "function":"linear",
    "decay":"10",
    "minimum":"10",
    "type": "dynamic", 
    "connection_info": challenge_config["connection-info"], 
    "attribution": challenge_config["attribution"], # should this be in the patch below? 
    "max_attempts": 0, # is this the default? does this mean unlimited? 
}

r = session.post(f"{CTFD_URL}/api/v1/challenges", json=create_challenge_payload, timeout=60)
r.raise_for_status() # if HTTP status code of response indicates an error (e.g. 4xx or 5xx), `raise_for_status()` will raise a `requests.exceptions.HTTPError` #TODO: handle this gracefully 
create_challenge_response = r.json()

CHALLENGE_ID = create_challenge_response["data"]["id"]
# then have to call patch endpoints with static assets + the rest of the fields 


# POST /api/v1/flags -> need challenge id 

create_challenge_flag_payload = {
    # TODO: figure out the difference between all these fields 
    "challenge_id": CHALLENGE_ID, 
    "type": "string", 
    "content": challenge_config["flag"], 
    "data": "", 
}
r = session.post(f"{CTFD_URL}/api/v1/flags", json=create_challenge_payload, timeout=60)
r.raise_for_status() # if HTTP status code of response indicates an error (e.g. 4xx or 5xx), `raise_for_status()` will raise a `requests.exceptions.HTTPError` #TODO: handle this gracefully 
# create_flag_response = r.json()


# POST /api/v1/tags -> need challenge id 
for tag in challenge_config["tags"]: 
    create_tag_payload = { 
        "challenge": CHALLENGE_ID, 
        "value": tag,   
    }
    r = session.post(f"{CTFD_URL}/api/v1/tags", json=create_tag_payload, timeout=60)
    r.raise_for_status() 

# POST /api/v1/hints -> need challenge id 
print(challenge_config["hints"])
for hint_index, hint in enumerate(challenge_config["hints"], start=1): 
    create_hint_payload = {
        "challenge_id":CHALLENGE_ID,
        "content": hint,
        "cost":0,
        "title": f"Hint {hint_index}",
        "requirements": {
            "prerequisites":[]
        }
    }
    r = session.post(f"{CTFD_URL}/api/v1/hints", json=create_hint_payload, timeout=60)
    r.raise_for_status() 

# POST /api/v1/files -> need challenge id 


# update the existing_challenges map at the end  
