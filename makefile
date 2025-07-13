teleportUrl=april-amex-poc.teleport.sh

tbot-setup:
	tctl bots rm example-bot
	tctl create -f workload-identity.yaml
	tctl create -f workload-identity-issuer-role.yaml
	tctl bots add --roles example-issuer example-bot
	echo "UPDATE CONFIG YAML WITH TOKEN"

tbot-run:
	tbot start -c config.yaml

auth:
	tsh login --proxy=$(teleportUrl) --user=admin

python-setup:
	python3 -m venv env
	source env/bin/activate
	pip install -r requirements.txt

server-run:
	export SPIFFE_ENDPOINT_SOCKET=unix:///tmp/tbot-user/workload.sock
	python3 spiffe-server.py

client-run:
	export SPIFFE_ENDPOINT_SOCKET=unix:///tmp/tbot-user/workload.sock
	python3 spiffe-client.py

workloadApiClient-run:
	export SPIFFE_ENDPOINT_SOCKET=unix:///tmp/tbot-user/workload.sock
	python3 workload-client-api.py