# git2ctf

`git2ctf` provides a GitOps-based infrastructure to automatically deploy CTF challenges.

```
/challenges
    /web
    /pwn
    /misc
```

# Brainstorm

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

- instantiator - manually deployment for challs needing instantiaor
- how to specify if you need ynetd?

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

---

- PRs, only some ppl can commit to main
- can only merge PR into main if checks pass (if have docker compose, external port must be left as a template string, also docker containers must all build)
- pipeline triggered upon push to main
- need info.yamls (or the one that is used in ctfdcli)

#TODO:

- squash commit history + change from master to main as default
- should automatically scale VM if VM space is used up
