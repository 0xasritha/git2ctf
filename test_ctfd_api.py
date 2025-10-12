# pylint: skip-file 
import json 
import requests 
import uuid 

CTFD_URL = "http://localhost:8000"

CTFD_TOKEN = "ctfd_4ada4094eb01ab7e37aba83c077b68d900f5ce2d4649df7ee111cb16d8f0f7fa"

session = requests.Session()
session.headers.update({"Authorization": f"Token {CTFD_TOKEN}"})

# stored in env variable: "<ctfd-id> : <git2ctf-uuid>"
env = {} 

# CREATE CHALLENGE 
"""


challenge_name = "test-standard-to-dynamic"
challenge_payload = {
    "name": challenge_name,  
    "category": "asdf", 
    "type": "standard", # change this to dynamic
    "state": "hidden", 
    "description": "TODO!", 
}

r = session.post(f"{CTFD_URL}/api/v1/challenges", json=challenge_payload, timeout=60)
r.raise_for_status()
data = r.json()
print(data)

"""
challenge_name = "test-dyanmic"
challenge_payload = {
    "name": challenge_name,  
    "category": "lklkja", 
    "description": "TODO!", 
    "state": "hidden", 
    "initial":"100",
    #"function":"linear",
    #"decay":"10",
    # "minimum":"10",
    "type": "dynamic", # change this to dynamic
}

r = session.post(f"{CTFD_URL}/api/v1/challenges", json=challenge_payload, timeout=60)
r.raise_for_status()
data = r.json()
print(data)

"""

update_to_dynamic_payload = { 
    "type": "standard"
}

r = session.patch(f"{CTFD_URL}/api/v1/challenges/25", json=update_to_dynamic_payload, timeout=60)
r.raise_for_status()
data = r.json()
print(data)


"""
"""
id = data["data"]["id"]
env[id] = str(uuid.uuid4())

# UPLOAD FILES 
r = requests.post(
    f"{CTFD_URL}/api/v1/files",
    headers={"Authorization": f"Token {CTFD_TOKEN}"},
    files=[
    	("file", open("test.txt", mode="rb"))
    ],
    data={"challenge_id": id, "type": "challenge"},
)
print(r.json())
"""
