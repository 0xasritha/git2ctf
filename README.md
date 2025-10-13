# git2ctf

`git2ctf` provides a GitOps-based infrastructure to automatically deploy CTF challenges.

```
/challenges
    /web
    /pwn
    /misc
```

# Latest Brainstorm

info.yaml:

```
uuid:
display-name-on-ctfd:
description:
tags:
author:
flag:
connection-info: "{{ HOST }}:{{ PORT }}"
```

- test the "credibility of the CTFd API" -> does it give me good error messages if I try to do something illegal (like move from static to dynamic)

- testing:
  - internal server error when I try to create a dynamic challenge without all fields specified

- branches need to be named: `<category-name>/<challenge-name>`
- upon commits to main:
  - parse all the info.yaml's within each challenge
  - then push them to CTFd
  - new or existing categorized based on UUIDs
    - have simple Python scripts for this?
    - if a new uuid within the info.yaml: create a POST request with the new challenge with the rest of the fields filled in by the defaults
    - if an existing challenge (uuid already exists): create a PATCH for those fields, or if category name changes
  - then deploy them

- would have to store a map of UUIDs to CTFd id's

- all the above fields locked down in CTFd, create "an alternative page" that admins can view to overwrite?

- port over all the stuff
- figure out the static file uploads stuff and zipping

- in the docs somewhere, mention looking at docker logs for the ctfd container as method of debugging
  - lets you change static->dynamic challenges without error (but has empty values for some of the required dynamic values)
  - however, does NOT let you change from dynamic->static (has internal server error, can look in the Docker logs)
  - for dynamic challenges: it will throw an internal error when the initial value ("initial") is not provided -> but I should just fill in all 4 dynamic fields to be safe

- put it through some sort of YAML sanitizer to make sure everyone has consistent YAML specs?
- how to track CTFd changes as a subrepo
- in documentation, put how infra team can add new categories easily

MVP Goal:

- get the new `info.yaml` working (what I have defined now) for both creating challenges + updating them, dynamically update connection info
  - static file assets
- get the pipeline working for deploying challenges onto VMs
  - doesn't have to provide live log streaming
- docs ?
- port over the current repo for mintueman to the new format
- PR checks
  - at the very least, do the port shit
  - the most basic checks
- update the CTFd visually so it makes stuff readonly

# Old Brainstorm

Local Testing:

- `admin`
- `password`

**Stage 1(MVP)**:

- bash script with GCP commands for spinning up infra (at first) -> or make this into a pipeline idk

chall deploying pipeline stuff:

- manually create DNS records for each "category" (`web.umasscybersec.org`), challenges are accessed based on port
- no automated subdomains, all challenges are on a different external port
- "template string" for external ports on docker compose, pipeline fills in ports
  - keeps track of "taken" ports via Github Actions Variable
  - automatically edit firewall rule to open that port? (might be manually just to specify a range at first for each category)
- run gcloud command via a "secret" or wtv (simplest way)
  - just SSH into VMs
- need `docker-compose` with "restart: unless-stopped"
  - have some sort of "base" docker-compose file that overwrites anything in the "child" docker files? (prolly later stage thing?)
- manually will output the connection information if you wanna store it in CTFd
- only re-scp + docker build etc. files if there has been any changes in that directory

if a commit includes a <category>/<challenge>/docker-compose.yaml (account for variations in which compose.yaml NAME (ie. yaml vs yml) can be written),
replace all external ports with ${xxx}
create a record for it in its internal port-tracker github actions environment variable - nextFreePort in range per category?
create a .env with that value when it is scped over onto the machine with that value (that way user is unable to touch anything, doesn't matter what they do)

look at ALL external ports it’s mapped too. If it is mapped to an external port, check if that is logged in the global environment variable. If it is different from what is already there, throw an error. Otherwise should be the template string or empty, if template string, see which ports are available for that category, then assign it, and update docker compose template to have the port. Then push

**Stage 1.5**:

- should deploy to multiple VMs instead of just one giant VM (both `/infra/gcp.sh` + the pipeline has to be updated)
- understand the mutex shit in the deploy workflow is that how we wanna do it??
- instantiator - manually deployment for challs needing instantiaor
- how to specify if you need ynetd?
- instead of opening all ports in the firewall rule, edit the firewall rule as each challenge deploys to accept traffic on that port as well in the pipeline
- dns record updates

**Stage 2**:

- VPN (Tailscale?)
- use Traefik (with "template strings" in the Docker compose files for labels??) for automated routing based on subdomains
  - binding to a public port in dokcer compose should no longer be necessary (confirm this)
- automated creation of DNS records for subdomains (ex. `guessy-chall.web.umasscybersec.org`)
- hooked up to ctfdcli (or om's one) for infra admins

**Stage 3**:

- deletion/cleanup logic?
- can specify if you need instantiaon, should automatically deploy ur challenge with instantiation if this is specified
- connect to remote docker deamon securely, that's how challenges are deployed
- automated resource management - for GCP atleast -> collect stats on if VMs available to deploy to, spin up another one or scale horizonctally if needed (automated as pipeline step)
- also deploy challenges to a dashboard that shows status on if they are up or not + discord bot? (automated as pipeline step)
- rn just using a service account for deploying shit in a gh action + create a gh workflow for this instead of a bash script?

---

- PRs, only some ppl can commit to main
- can only merge PR into main if checks pass (if have docker compose, external port must be left as a template string, also docker containers must all build)
- pipeline triggered upon push to main
- need info.yamls (or the one that is used in ctfdcli)

#TODO:

- squash commit history + change from master to main as default
- should automatically scale VM if VM space is used up
