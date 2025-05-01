# Teleport Workload Identity Example Replaces SPIRE

## Introduction

In this repositiory, there are three examples of using Teleport to provide SPIFFE SVIDs to client applications. Each of them utilizes the *Workload API* (https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/#spiffe-workload-api) as a Unix domain socket. Teleport's `tbot` Machine ID bot provides the domain socket and is configured to provide a specific set (1 or more) SVIDs over that socket. This functionality is available in all edition of Teleport.

All examples assume some basic knowledge of Teleport operations and tools (`tsh` and `tctl`). Getting started guides for Teleport are available in the TEleport documentation here: https://goteleport.com/docs/get-started/. 

The example deployemnts are:
 - A standard application running on a machine (or VM). In this scenario, `tbot` is running on the same machine and providing the WorkloadAPI endpoint on the file system. These two Python (module: py-spiffe) are native SPIFFE applications, ie. the SPIFFE enablement is in the application code itself.
 - A single Kubernetes pod deployment having `tbot` as a sidecar in the pod. This example uses CNCF **Envoy Proxy** as a sidecar proxy to handle the SPIFFE interactions. The application, in this case, **does not need to be altered.**
 - A "cluster wide" Kubernetes WorkloadAPI endpoint provided utilizing the CNCF **SPIFFE CSI Driver** (https://github.com/spiffe/spiffe-csi) to allow the WorkloadAPI endpoint to be mounted in more than one pod across the whole cluster.

## Single Pod & Sidecar Deployment in Kubernetes

## WorkloadAPI "Cluster Wide" Deployment in Kubernetes

## Single Machine Client and Server Example

This complete example can be run on a single machine, including your laptop. To show the complete functionality, three terminal windows (or tabs) will be needed: one for "tbot" and two for the client/server pair of appilcations. The example depends on all three being run on the same host (to limit the number of "tbot" instances running) using the standard Unix domain socket for SPIFFE requests from both applications.

![SPIFFE without SPIRE](https://github.com/user-attachments/assets/7db6d767-0bb2-476a-b3a3-7107701c132c)


### Initialize Teleport environment

`git clone pfcurtis/teleport-workload-example` (this repository)

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


