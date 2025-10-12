
# TODO: WOULD MAKE MOST SENSE FOR HINT, TAG, AND FLAG OBJECTS TO JUST DELETE IT AND REMAKE THEM I THINK 
# POST /api/v1/tags -> need challenge id 
"""
for tag in challenge_config["tags"]: 

create_tags_payload = { 
    "challenge": CHALLENGE_ID, 
    "value": 
}
"""

r = session.get(f"{CTFD_URL}/api/v1/challenges/31/tags", json=create_challenge_payload, timeout=60)
r.raise_for_status() 
print(r.json())

