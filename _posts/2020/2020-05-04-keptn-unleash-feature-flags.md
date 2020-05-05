---
layout: post
title: Keptn + Unleash = Automated Feature Flag Self Healing for Non Kubernetes Environments
header_image: /images/headerimages/unleash_keptn.png
categories: [unleash, keptn, feature flag, self healing, automation]
---

[Keptn](https://keptn.sh) is an event-based control plane for continuous delivery and automated operations. [Unleash](https://unleash.github.io) is a feature toggling framework. It sounds like these two would play well together, even in non-cloud native environments...

# Overview

> Self healing software is a cornerstone in software automation maturity. Tooling comes second to the ability and willingness to change the way you create software.

Keptn already has an [excellent tutorial](https://keptn.sh/docs/0.6.0/usecases/self-healing-with-keptn/dynatrace-unleash/) on running Keptn & Unleash in Kubernetes or OpenShift based environments. The focus of this post is how we can leverage these components in a **non-Kubernetes environment**.

This post will create an application that is coded to include feature flag capability. While **disabled**, the application will deliver traffic in the normal operating mode ie. serving the content from the application itself. When the feature flag is **enabled**, the application will instead serve traffic from a static resource (a file hosted on a CDN).

The feature flag engine that makes this possible will be Unleash.

Keptn will be the orchestration layer responsible for reacting to "problem events" and self healing the application by enabling the feature flag.

This scenario is used in real-world scenarios when websites wish to include a safety switch that they can toggle in case of emergencies (traffic overload, DDoS attack etc.)

Rounding out the system will be a monitoring provider. The monitoring providers job is to inform Keptn whenever there is a problem with the system (in our demo, an increased server-side error rate).

Keptn can use metrics from any third party tool, the two most common being [Prometheus](https://prometheus.io) or [Dynatrace](https://dynatrace.com). For this demo, we will use Dynatrace.

# Fast Developer Feedback
Not only is it important to have self healing software, but it's imperative that the developers get instant feedback on their code. For this reason, Keptn automatically pushes a stream of comments on to the Dynatrace problem ticket whenever a remediation step is attempted / performed. In this way, the developers can understand exactly what led up to the issue & how Keptn resolved the issue. 

# Architecture & Sequence Diagram

Here is the system architecture and sequence of events:

1. Application is monitored by Dynatrace.
1. We will manufacture an increase in error rate to simulate a production issue.
1. Dynatrace identifies the issue and sends a notification to Keptn.
1. Keptn triggers the remediation workflow and informs Unleash to toggle the feature flag to "on". Traffic is now served [from the CDN](https://raw.githubusercontent.com/agardnerIT/OddFiles/master/index2.html) rather than the app.
1. Keptn notifies the monitoring solution (Dynatrace) of the remediation attempt.

![architecture and sequence diagram](/images/postimages/keptn-unleash-1.png)

# Prerequisites

- A Dynatrace tenant ([free trial available here](https://dynatrace.com/trial/))
- A [full Keptn installation](https://keptn.sh/docs/quickstart)
- [Dynatrace monitoring and the Dynatrace SLI Provider](https://keptn.sh/docs/0.6.0/reference/monitoring/dynatrace/) installed and configured on the Keptn machine.
- An Ubuntu VM used to host your website and the Unleash Feature Flag service.

Any linux based VM will work, but you will have to modify the instructions to suit your distro.

# Networking Prerequisites
For this demo:
- The `keptn` VM will need to allow inbound HTTPS traffic from Dynatrace SaaS.
- The `application` VM (running `proxy`, `app`, `unleash` and `postgres`) will need to allow inbound HTTP traffic from the `keptn` machine.

# Containers?

I have chosen to deploy these workloads as containers purely for ease during the demo setup. There is **nothing** here that could not be achieved without using containers.

In terms of the demo and outputs, you may entirely ignore the fact that the application and Unleash service are running in containers. It makes no difference to the end result.

# Install & Configure Git and Docker

On the application VM, run the following:

```
sudo apt update && sudo apt install git docker.io -y
sudo usermod -aG docker $USER
```

Launch a new terminal window to pick up the new user permissions. Validate it works with `docker ps`

You should see:

```
CONTAINER ID    IMAGE    COMMAND    CREATED    STATUS    PORTS    NAMES

```

# Clone This Repo
```
git clone https://github.com/agardnerit/unleashtutorial
cd unleashtutorial && chmod +x loadGenErrors.sh
```

# Create New Docker Network
This allows containers to talk to each other via their container name.

On the application VM, run the following:

```
docker network create agardner-net
```

# Run a PostGresDB for Unleash

On the application VM, run the following:

```
docker run -d --name postgres --network agardner-net -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=unleash postgres
```
Database = `unleash`
Username = `postgres`
Password = `mysecretpassword`

# Build & Run the Unleash Container

On the application VM, run the following:

```
docker build -t unleash ./unleash && docker run -d --name unleash --network agardner-net -e DATABASE_URL=postgres://postgres:mysecretpassword@postgres:5432/unleash unleash
```

# Build and Run the App

On the application VM, run the following:

```
docker build -t app . && docker run -d --name app --network agardner-net app
```

# Build and Run the NGINX Reverse Proxy

On the application VM, run the following:

```
docker build -t proxy ./proxy && docker run -d -p 80:80 --name proxy --network agardner-net -e DT_CUSTOM_PROP="keptn_project=website keptn_service=front-end keptn_stage=production" proxy
```

# Validate Containers

Running `docker ps` should show 4x containers: `proxy`, `app`, `unleash` and `postgres`.

```
CONTAINER ID    IMAGE   ...  PORTS                NAMES
c1344de4e69c    proxy        0.0.0.0:80->80/tcp   proxy
676935d87028    app                               app
be6937f7641c    unleash      4242/tcp             unleash
fee962f54612    postgres     5432/tcp             postgres
```

# Validate User Interfaces

- The Unleash UI should now be available on `http://<APP-VM-IP>/unleash`
- The app should now be available on `http://<APP-VM-IP>`

Validate that both of these are available by visiting them in a browser.

You can login to unleash with **any username & password**.

![unleash ui](/images/postimages/keptn-unleash-2.png)

![app ui](/images/postimages/keptn-unleash-3.png)

# Validate Dynatrace Tags

In your Dynatrace tenant, open the `Transactions and Services` page, select the `Keptn website production` management zone to filter your services and navigate to the `unleash-demo` service.

Ensure that your service is tagged with the following:

`keptn_project:website`, `keptn_service:front-end` and `keptn_stage:production`

![dynatrace tags](/images/postimages/keptn-unleash-5.png)

These tags are created when you [installed the Dynatrace service on Keptn](https://keptn.sh/docs/0.6.0/reference/monitoring/dynatrace) . If you do not see these tags, please **STOP** and ensure you follow this instructions linked above.

This tutorial **WILL NOT WORK** without these tags.

# Validate Problem Notification Integration

Keptn automatically configures the problem notification integration when you onboard the Dynatrace Service.

Validate that it's available now. In Dynatrace, go to `Settings > Integration > Problem Notifications` and you should see an entry for Keptn. If you do not see this problem notification, **STOP** and ensure you've installed Dynatrace on the keptn box.

![dynatrace tags](/images/postimages/keptn-unleash-6.png)

This tutorial **WILL NOT WORK** without this integration.

# Configure Problem Sensitivity
For demo purposes, we will set Dynatrace to be extremely sensitive to failures.
Find the `unleash-demo:80` nginx service, edit the anomaly detection settings and adjust the settings to match these:

![dynatrace tags](/images/postimages/keptn-unleash-7.png)

# Create Feature Flag
- Go to `http://<APP-VM-IP>/unleash` and login (use any fake values you like to login)
- Create a feature flag called `EnableStaticContent` (case sensitive and must be called this).
- Set the flag to `disabled`
- Refresh the application UI and you should still see the standard (blue bar) page.

![unleash ui with feature flag](/images/postimages/keptn-unleash-4.png)

![application standard ui](/images/postimages/keptn-unleash-2.png)

# Manually Test Flag
Prove that the feature flag works:

- Go to the app (`http://<APP-VM-IP>`) and refresh the page. You should still see the blue banner. This page is served from the `app` container.
- Enable the feature flag and refresh the app. Notice the green banner, this page is served from GitHub.

![application CDN ui](/images/postimages/keptn-unleash-8.png)

<br />

Set the flag back to `disabled` so that traffic is being served by the app (blue banner).

<br />

![application standard ui](/images/postimages/keptn-unleash-2.png)

# Clone Repo to Keptn Machine, Create Keptn Project & Service

Execute these commands on the Keptn cluster:

```
cd ~
git clone http://github.com/agardnerit/unleashtutorial
cd unleashtutorial
keptn create project website --shipyard=shipyard.yaml
keptn create service front-end --project=website
keptn add-resource --project=website --service=front-end --stage=production --resource=remediations.yaml --resourceUri=remediation.yaml
```

The values in the `remediations.yaml` file tell Keptn how to respond when it sees a failure rate increase problem for this project (`website`), service (`front-end`) and stage (`production`)

# Create Secret & Bounce Remediation Service
Note that the `username` and `token` can be set to anything.

The `remediation-service` pod must be recreated so that it picks up this new secret.

Execute these commands on the Keptn cluster:

```
kubectl create secret -n keptn generic unleash --from-literal="UNLEASH_SERVER_URL=http://<APP-VM-IP>/unleash/api" --from-literal="UNLEASH_USER=me" --from-literal="UNLEASH_TOKEN=whatever"
kubectl delete pod -n keptn -l "run=remediation-service"
```

# Load Generator

> Run this on the application VM hosting the website.

Run the load generator which will create errors. In another tab, keep refreshing the page and in a few minutes (when DT raises a problem) you'll see the website failover to the green static hosted content.

```
cd ~/unleashtutorial
./loadGenErrors.sh
```

- You will see `HTTP 500` errors being shown. The failure rate registered by Dynatrace on the `unleash-demo:80` service will also increase.

```
$ ./loadGenErrors.sh 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
-----------------
```

- After about 10 minutes, Dynatrace will register a problem and push a notification to Keptn.
- The Keptn `remediation-service` will activate and toggle the feature based on the `remediations.yaml` file.
- The feature flag will be `enabled` and the CDN page will be served (from GitHub) ([this is the actual page](https://github.com/agardnerIT/OddFiles/blob/master/index2.html))

![unleash toggle enabled](/images/postimages/keptn-unleash-9.png)

![application CDN ui](/images/postimages/keptn-unleash-8.png)

# Conclusion

Although Keptn and Unleash are primarily designed for Kubernetes-based environments, there is no reason they (and the automation concepts described) cannot be used in a non-containerised environment.

> Willingness to change the way you design and write software. Willingness to empower developers. Ability to quickly get relevant, actionable feedback to developers. Three key ingredients to a successful automation strategy.

Tooling helps, but culture is much more important on your software automation journey. The three big ones are:

1. A willingness (and ability) to rething the way you design and write software.
1. A willingness to empower your development teams to take responsibility for the code they produce.
1. The ability to get relevant, actionable feedback to developers - quickly.