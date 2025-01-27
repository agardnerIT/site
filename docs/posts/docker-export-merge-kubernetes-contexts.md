---
layout: post
title: Export Kube Config From Docker Container and Merge
categories:
- kubernetes
date:
  created: 2022-03-12
---

How to export a kubernetes config context file from inside a docker container, to the host and merge.

<!-- more -->

## Introduction

If you use Docker in Docker (`dind`) or Kubernetes in Docker (`kind`) you will end up with a `kubectl` running inside a docker container but you probably also want to interact using `kubectl` from localhost.


## Export Contexts

Use the `docker cp` command to copy the kube config file from the container to the localmachine:

```
docker cp YourContainerName:/UsernameTheContainerIsUsing/.kube/config ./config
```
For example:

```
docker cp mycontainer:/root/.kube/config ./config
```

Ensure the config points to the correct endpoint.  Modify the `config` file and adjust the `server` field. You might have:

```
server: https://host.docker.internal:39155
```

Whereas `host.docker.internal` won't resolve from the host machine so that needs to be:


```
server: https://127.0.0.1:39155
```

Trial and error is probably required here.

## Merge Contexts

Now merge any existing `kubectl` config file and this new one. The syntax is:

```
export KUBECONFIG=ExistingFile:NewFile
```

For example:

```
export KUBECONFIG=~/.kube/config:~/config
```

Finally use kubectl to merge and flatten the two configs:

```
kubectl config view --merge --flatten > ./mergedconfigs && mv ./mergedconfigs ~/.kube/config
```

Verify that configs are merged:

```
kubectl config get-contexts
```

For example:

```
CURRENT   NAME             CLUSTER          AUTHINFO            NAMESPACE
*         docker-desktop   docker-desktop   docker-desktop      
          k3d-mykeptn      k3d-mykeptn      admin@k3d-mykeptn  
```

## Try It Out

Switch to your new context:
```
kubectl config use-context k3d-mykeptn
```

Now try it. From your localhost:

```
kubectl get ns --context=YourNameContext
```