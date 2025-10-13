import os 
import sys 

from pathlib import Path
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE") or sys.exit("GITHUB_WORKSPACE is not set")
CHALLENGE_PATH = os.getenv("CHALLENGE_PATH") or sys.exit("CHALLENGE_PATH is not set")
full_challenge_dir_path = os.path.join(GITHUB_WORKSPACE, CHALLENGE_PATH)
bad_names = [
    "docker-compose.yaml",
    "docker-compose.yml",
   "compose.yml",
]
for name in bad_names:
    if os.path.isfile(os.path.join(full_challenge_dir_path, name)):
        print("FAIL")
        sys.exit(1)
print("PASS")
