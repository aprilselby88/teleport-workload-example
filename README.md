## Teleport Workload Identity Example Replaces SPIRE

The example is designed to utilize off-the-shelf SPIFFE libraries, in this case `py-spiffe`, for a simple client/server interaction. The example also demonstrates the method to have multiple applications running on the same machine or in the same Kubernetes pod share a single Teleport "tbot" instance. 

This complete example can be run on a single machine, including your laptop. To show the complete functionality, three terminal windows (or tabs) will be needed: one for "tbot" and two for the client/server pair of appilcations. The example depends on all three being run on the same host (to limit the number of "tbot" instances running) using the standard Unix domain socket for SPIFFE requests from both applications.

![Architecture diagram](https://github.com/pfcurtis/teleport-workload-example-python/blob/main/Simple_SPIFFE_Diagram.png)

### Initialize Teleport environment

`git clone pfcurtis/teleport-workload-example-python`

`cd teleport-worload-example-python`

Authenticate using `tsh`

`tctl bots rm example-bot`

`tctl create -f workload-identity.yaml`

`tctl create -f workload-identity-issuer-role.yaml`

`tctl bots add --roles example-issuer example-bot`

Edit `config.yaml` with your proxy and the token from the above `bots add`

`tbot start -c config.yaml`


### Initialize Python environment

`python3 -m venv env`

`pip install -r requirements.txt`

In each window (ot terminal tab)

`export SPIFFE_ENDPOINT_SOCKET=unix:///tmp/tbot-user/workload.sock`

Then run the application of choice.
* spiffe-server.py (server side)
* spiffe-client.py (client side)
* workload-client-api.py (lists all the SVIDs available from the current running "tbot")


