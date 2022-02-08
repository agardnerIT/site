---
layout: post
title: Keptn Hello World
categories: [keptn]
---

The Keptn "Hello World" example in under 10 minutes.

## Introduction

There are lots of excellent tutorials on the Keptn website but this post aims to get you up and running with Keptn and a "Hello World" example in under 10 minutes.

## What You Will Need

To follow along, you will need:

1. A GitHub account
1. A Kubernetes Cluster
1. Helm installed

## Create GitHub Stuff

1. Create a GitHub PAT with full `repo` scope. Keptn will use this token to ensure all files and changes are synced to the upstream repo.
1. Create a blank (uninitialised) repository for Keptn to work with. Do not add any files (not even a readme)
1. Set some environment variables like below

```
export GIT_USER=<YourGitUsername>
export GIT_REPO=https://github.com/<YourGitUserName>/<YourRepo>
export GIT_TOKEN=ghp_****
```

## Install and Expose Keptn
```
curl -sL https://get.keptn.sh | KEPTN_VERSION=0.12.0 bash
helm install keptn https://github.com/keptn/keptn/releases/download/0.12.0/keptn-0.12.0.tgz -n keptn --create-namespace --wait
```

All pods should now be up and running: `kubectl get pods -n keptn`

```
NAME                         READY   STATUS
bridge-*                     1/1     Running
approval-service-*           2/2     Running
api-gateway-nginx-*          1/1     Running
webhook-service-*            2/2     Running
lighthouse-service-*         2/2     Running
keptn-mongo-*                1/1     Running
remediation-service-*        2/2     Running
configuration-service-*      1/1     Running
secret-service-*             1/1     Running
keptn-nats-cluster-0         2/2     Running
api-service-*                2/2     Running
mongodb-datastore-*          2/2     Running
shipyard-controller-*        2/2     Running
statistics-service-*         2/2     Running
```

Continue:
```
helm install -n keptn job-executor-service https://github.com/keptn-contrib/job-executor-service/releases/download/0.1.6/job-executor-service-0.1.6.tgz --wait
```

This will add one extra pod:

```
NAME                      READY   STATUS
job-executor-service-*    2/2     Running
```

Expose Keptn:
```
curl -SL https://raw.githubusercontent.com/keptn/examples/master/quickstart/expose-keptn.sh | bash
```

Temporary Note: If running on localhost, that script will work perfectly. If running on a cloud provider with Load Balancers available, the script above will point to `http://127.0.0.1` which obviously isn't correct. To fix, run the following to expose the bridge (UI) on a loadBalancer. We're working on a fixed script and I will remove this step once merged.

```
helm upgrade keptn https://github.com/keptn/keptn/releases/download/0.12.0/keptn-0.12.0.tgz -n keptn --set=control-plane.apiGatewayNginx.type=LoadBalancer --wait
export KEPTN_ENDPOINT=$(kubectl get services -n keptn api-gateway-nginx -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Keptn Available at: http://$KEPTN_ENDPOINT"
keptn auth --endpoint=$KEPTN_ENDPOINT
```


## Configure Keptn
```
wget https://gist.githubusercontent.com/agardnerIT/8046b8a81bab90a37aef83219a8e8078/raw/341b6d3c8b8dfab30742320402706e903e5bb4ab/shipyard.yaml
keptn create project hello-world --shipyard=shipyard.yaml --git-user=$GIT_USER --git-remote-url=$GIT_REPO --git-token=$GIT_TOKEN
keptn create service demo --project=hello-world
wget https://gist.githubusercontent.com/agardnerIT/1d4eaa1425832ee9a9036de92a20b3b7/raw/c0caddfcc3025fb16b55b21ea683ed7f1be328fe/jobconfig.yaml
keptn add-resource --project=hello-world --service=demo --stage=dev --resource=jobconfig.yaml --resourceUri=job/config.yaml
```

## Trigger Keptn

Trigger Keptn by sending a cloudevent to the API using the `keptn send event` command. A precrafted cloudevent is available for you:

```
wget https://gist.githubusercontent.com/agardnerIT/005fc85fa86072d723a551a5708db21d/raw/d9efa71969657f7508403f82d0d214f878c4c9ca/hello.triggered.event.json
keptn send event -f hello.triggered.event.json
```

Go to the Keptn bridge, into the sequence view of the `hello-world` project and you should see:

![keptn sequence run success](/images/postimages/keptn-hello-world-1.jpg)

## What Happened?

Keptn core components were installed along with the `job-executor-service` microservice. The `keptn` CLI was also downloaded. The Keptn bridge was exposed and, to make this demo easier, all authentication was removed.

A Keptn project was created called `hello-world` and a shipyard file was provided. A shipyard file is the "blueprint" of a Keptn project.  Inspect this file. Notice it has one stage (`dev`), one sequence (`hello`) and this sequence has one task associated to it (`hello-world`). A Keptn service was created called `demo`.

The job executor service comes preconfigured to listen for all Keptn events.

The `job/config.yaml` file instructs the job-executor-service microservice to run the `alpine` docker image and run `echo "hello world"` when it "hears" the `sh.keptn.event.hello-world.triggered` event.

The `keptn send event` is a wrapper around the Keptn API endpoint. The cloudevent asks Keptn to trigger the `hello` sequence in the `dev` stage of the `hello-world` project for the `demo` service.

## Wait! I triggered `hello`, not `hello-world`?

Correct: You triggered the `sequence` and Keptn handles the `task` execution for you.

> Humans (or other tooling) trigger Keptn sequences. Tooling responds to Keptn tasks.

Due to the shipyard file, Keptn knows that the first task in your sequence is called `hello-world` so:

1. Keptn crafts a cloud event for you and distributes it to whatever service is listening for the `sh.keptn.event.hello-world.triggered` event
1. In our case, the job executor service is configured to respond. The JES looks up the config from the yaml file and runs the container
1. The job executor service sends a pair of events back to Keptn (a `.started` and corresponding `.finished` event)
1. Keptn receives a matching pair of `.started` and `.finished` events from JES so knows the task is done
1. Keptn now finishes the sequence


## What's the big deal?

> Keptn handles the orchestration and timing, you bring the tools you already use.

You've successfully split the process from the tooling. You've hidden the complexities of tooling API interaction. There are thousands of tool integrations already written for Keptn or write your own. Keptn comes out-of-the-box with microservices dedicated to self-healing and code quality gate workflows.

With Keptn it is incredibly easy to build complex task sequences whilst no longer worrying about the tooling that will implement those tasks.

- Try adding further tasks to your sequence
- Try sending a webhook to a third party tool instead of using the job executor service
- Build a full end-to-end delivery pipeline or any other sequence of tasks you can dream up

## Next Steps

1. Continue to explore Keptn on the [public demo system](https://tutorials.keptn.sh/tutorials/keptn-public-demo-011/index.html)
1. Use Keptn for multi-stage delivery or self-healing with [Prometheus](https://tutorials.keptn.sh/tutorials/keptn-quickstart-011/index.html)
1. Use [Keptn to orchestrate Argo Rollouts](https://tutorials.keptn.sh/tutorials/keptn-argo-rollouts-dynatrace-11-on-k3s/index.html)
1. Use [Keptn for Resilience evaluation with LitmusChaos](https://tutorials.keptn.sh/tutorials/keptn-litmus-011/index.html)
1. Explore the [tools and integrations](https://keptn.sh/docs/integrations/) that Keptn currently supports

Got questions? Need help? Join the [Keptn community on Slack](https://slack.keptn.sh)