# assume you are already authenticated with gcloud CLI 

# create VM called `challs` (`us-east1`, `us-east1-b`, `e2-standard-2` (2 vCPU, 1 core, 8 GB memory), 25 GB, ~$52)

# install docker + git on that VM 

# give `challs` static, external IP 

# create a firewall rule (`allow-challs-traffic`) that matches on any tag `challs`, allows all traffic (TODO: fix)   

# edit the VM to have the `challs` tag 

# create a static assets bucket (`minutemanctf25-challenge`) with public viewing permissions + should download  static assets (https://cloud.google.com/storage/docs/access-control/making-data-public#console)

# create the service account (for github actions) (`git2ctf-minutemanctf25`)
# IAM & ADMIN > Service accounts > + Create service account; give it "Owner" permissions (TODO: fix)
# after creating it, click on it, go to the "Keys" page, and then generate a JSON 

# OUTPUTS TO BE CREATED AS A REPOSITORY SECRET: 
# GCP_CREDENTIALS: contents of the service account JSON file 
