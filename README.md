#!/bin/bash


git clone <xxx>/teleport-worload-example-python

cd teleport-worload-example-python

Authenticate using `tsh`

tctl bots rm example-bot

tctl create -f workload-identity.yaml

tctl create -f workload-identity-issuer-role.yaml

tctl bots add --roles example-issuer example-bot

Edit `config.yaml` with your proxy and the token from the above `bots add`
tbot start -c config.yaml


Initialize Python environment

python3 -m venv env
pip install -r requirements.txt

export SPIFFE_ENDPOINT_SOCKET=unix:///tmp/tbot-user/workload.sock 

