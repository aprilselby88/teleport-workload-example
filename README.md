# Teleport Workload Identity Example Replaces SPIRE

## Introduction

In this repositiory, there are three examples of using Teleport to provide SPIFFE SVIDs to client applications. Each of them utilizes the **Workload API** (https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/#spiffe-workload-api) as a Unix domain socket. Teleport's `tbot` Machine ID bot provides the domain socket and is configured to provide a specific set (1 or more) SVIDs over that socket. This functionality is available in all editions of Teleport.

All examples assume some basic knowledge of Teleport operations and tools (`tsh` and `tctl`). Getting started guides for Teleport are available in the Teleport documentation here: https://goteleport.com/docs/get-started/.

In order for the Teleport `tbot` to register with the Teleport cluster, an initial join token must be created and/or provided. In the simple machine example below, a join token is requested manually (static token). For the two Kubernetes examples, Kubernetes secret tokens are used. See https://goteleport.com/docs/reference/join-methods/ for explanations of these two diffent types of join tokens and their limitations.

**WorkloadAPI** attestation with Teleport `tbot` is explained here: https://goteleport.com/docs/reference/workload-identity/workload-identity-api-and-workload-attestation/

The example deployemnts are:
 - A standard application running on a machine (or VM). In this scenario, `tbot` is running on the same machine and providing the **WorkloadAPI** endpoint on the file system. These two Python (module: py-spiffe) programs are native SPIFFE applications, ie. the SPIFFE enablement is in the application code itself.
 - A single Kubernetes pod deployment having `tbot` as a sidecar in the pod. This example uses **Envoy Proxy** as a sidecar proxy to handle the SPIFFE interactions. The application, in this case, **does not need to be altered.**
 - A "cluster wide" Kubernetes **WorkloadAPI** endpoint provided utilizing the **SPIFFE CSI Driver** (https://github.com/spiffe/spiffe-csi) to allow the **WorkloadAPI** endpoint to be mounted in more than one pod across the whole cluster. This example also uses the **Envoy Proxy** to handle the SPIFFE authorization.

In all three examples, Teleport workload identities and roles are created. (SPIFFE Verifiable Identity Documents [SVIDs] explained: https://spiffe.io/docs/latest/deploying/svids/) The same workload identity and roles are used by all three examples. In the `workload-identity.yaml` file, you will see the create of two SVIDs (`/svc/server` and `/svc/client`). Additonally, the individual identities have a label (`example: workload-example`). It is these labels that are used to grant access to the SVIDs in the Teleport role that is created:

```
spec:
  allow:
    workload_identity_labels:
      example: ["workload-example"]
```
Each instance of `tbot` providing a **WorkloadAPI** can then be assigned a role or roles that will provide the SVIDs that are required. This flexibility allows the SPIFFE deployment to scale easily.

## Examples

### Single Pod & Sidecar Deployment in Kubernetes

https://github.com/pfcurtis/teleport-workload-example/tree/main/kubernetes/single-pod

### WorkloadAPI "Cluster Wide" Deployment in Kubernetes

https://github.com/pfcurtis/teleport-workload-example/tree/main/kubernetes/spire-csi

### Single Machine Client and Server Example

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


