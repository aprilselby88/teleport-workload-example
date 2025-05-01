# SPIFFE CSI with Envoy Proxy Deployments

### `kubeconfig` Required

This is a collection of manifests and `tctl` command files. You will need to have a valid `kubeconfig` at the **cluster-admin** level in order to test this example. It has been tested using a **KIND** cluster.


### Initialize Teleport environment

`git clone pfcurtis/teleport-workload-example` (this repository)

`cd teleport-worload-example-python`

Authenticate using `tsh`

`tctl bots rm web-server`

`tctl create -f ../../workload-identity.yaml`

`tctl create -f ../../workload-identity-issuer-role.yaml`

`tctl bots add --roles example-issuer web-server`

### Apply Kuberneters manifests and `tctl` commands

`kubectl apply -f 00-create-ns.yaml`

`kubectl apply -f 01-create-rbac.yaml`

`kubectl apply -f 02-spiffe-csi-driver.yaml`

`tctl create -f 03-tctl-create-bot.yaml`

`kubectl proxy -p 8080`

`curl http://localhost:8080/openid/v1/jwks` (This captures the Kubernetes cluster public key for use in attestation) More complete instructions on editing the create bot token manifest with this key are here: https://goteleport.com/docs/enroll-resources/machine-id/deployment/kubernetes/#step-35-create-a-join-token

`tctl create -f 04-tctl-create-bot-token.yaml`

`kubectl apply -f 05-create-tbot-configmap.yaml`

`kubectl apply -f 06-tbot-daemonset.yaml`

`kubectl apply -f 07-create-envoy-configmap.yaml`

`kubectl apply -f 08-envoy-proxy-deploy.yaml`

`kubectl apply -f 09-web-server-deploy.yaml`
