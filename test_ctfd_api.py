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
#TODO: what other fields do we need to specify, probably the dynamic scoring stuff 
challenge_name = "test1"
challenge_payload = {
    "name": challenge_name,  
    "category": "Web Exploitation", 
    "type": "standard", # change this to dynamic
    "state": "hidden", 
    "description": "TODO!", 
    "max_attempts": 0, # unlimited, 
}

r = session.post(f"{CTFD_URL}/api/v1/challenges", json=challenge_payload, timeout=60)
r.raise_for_status()
data = r.json()
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


# # SEND A POST WITH THE UUID 
#
# extra_payload = {
#     "extra": { 
#         "git2ctf_uuid": "f9ec2919-cb2c-4fc5-9182-9b1bf5609403"
#     }
# } 
# print("UPDATING WITH EXTRA STUFF")
# r = session.patch(f"{CTFD_URL}/api/v1/challenges/{id}", json=extra_payload, timeout=60)
# r.raise_for_status()
# data = r.json()
# print(json.dumps(data, indent=2))
#

