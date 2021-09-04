---
layout: post
title: Getting Started with Keptn
header_image: /images/headerimages/TODO.jpg
categories: [keptn]
---


Keptn is a flexible workflow and automation engine. With that flexibility comes perceived complexity. However it is extremely easy to get started with Keptn. You can be up and running in under 10 minutes...

## Keptn 101: Getting Started in 3 Steps

1. Define **what** you want to achieve
2. Model that intention in a Shipyard file
3. Define the tooling that you want to use to achieve those tasks

## 1. Define Tasks

Start by deciding what you want to achieve. Split this work into two "levels": sequences and tasks.

The most simple example would be a desire to create a report. Most likely this is a very simple workflow consisting of a single "create report" task.

A more complex example may be that you wish to create a fully fledged sequence of tasks that build an entire demo system. In which case, the tasks you must run are:

1. Create infrastructure
2. Install application
3. Onboard a user
5. Notify user that they now have access to the demo system
6. Report to a third party system to record that the demo system is available

## 2. Model Your World

Keptn models the world in a file called a Shipyard YAML file. The values given below are examples only and things can be named however you wish.

We must now translate our requirements into a shipyard.yaml file:

Some quick FYIs:

1. Sequences (by default) are standalone
2. When a sequence is triggered to run, Keptn will automatically execute each task sequentially
3. Sequences can be linked together to build complex workflows
4. Metadata can be provided to each task either in the Shipyard or via the Keptn API when triggering a sequence


Define the basics of your shipyard:

```yaml
---
apiVersion: "spec.keptn.sh/0.2.2"
kind: "Shipyard"
metadata:
  name: "my-first-shipyard"
```

Now decide how many `stages` you want to model. In our case, we only need one as we're not modelling anything pipeline related (where things "move" from one "stage" to the next). So we'll call our stage `main`

```yaml
---
apiVersion: "spec.keptn.sh/0.2.2"
kind: "Shipyard"
metadata:
  name: "my-first-shipyard"
spec:
  stages:
    - name: "main"
```

Define your sequences and tasks. Modelling the simple `createreport` sequence might look like this, where we have a single sequence and a matching single task.

Remember that the name values can be any string you want, so you're free to make up your own sequence and task names.

```yaml
---
apiVersion: "spec.keptn.sh/0.2.2"
kind: "Shipyard"
metadata:
  name: "my-first-shipyard"
spec:
  stages:
    - name: "main"
    sequences:
      - name: "makereport"
        tasks:
          - name: "createreport"

```

The more complex "create a demo system" workflow might look like this:

```yaml
---
apiVersion: "spec.keptn.sh/0.2.2"
kind: "Shipyard"
metadata:
  name: "my-first-shipyard"
spec:
  stages:
    - name: "main"
    sequences:
      - name: "createdemosystem"
        tasks:
          - name: "createinfra"
          - name: "installapp"
          - name: "onboarduser"
          - name: "notify"
          - name: "report"
```

## 3. Define Your Tooling

It is now time to define the tooling you wish to execute each task. This tooling can take a number of forms:

1. An HTTP request to an endpoint, shell script or Python script
1. A container image that should run for a particular task
1. A more complex or custom workflow that's modelled by a "full Keptn service" (example: [JIRA Service](https://github.com/keptn-sandbox/jira-service))

You may decide that:

- `buildreport` task is best handled by running a Python file
- `createinfra` task is best handled by the `aws-service`
- `installapp` task is best handled by running a shell script
- `onboarduser` task is best handled by running the `example/someimage:1.0.2` container
- `notify` best handled by `slack-service`
- `report` best handled by `jira-service`

Tooling in Keptn listens for and reacts to `sh.keptn.event.{taskname}.triggered` event. Which events your service listens for is easily set via an environment variable when installing the service.

In the above example:

- Install the [generic executor service](https://github.com/keptn-sandbox/generic-executor-service) and configure the environment variable to listen for the `sh.keptn.event.buildreport.triggered` event
- Install the `aws-service` and configure the env var to listen for the `sh.keptn.event.createinfra.triggered` event
- Configure the [generic executor service](https://github.com/keptn-sandbox/generic-executor-service) to listen for a second event: `sh.keptn.event.installapp.triggered` event and run the shell script
- Install the [job executor service](https://github.com/keptn-sandbox/job-executor-service) and configure it to listen for the `sh.keptn.event.onboarduser.triggered` event
- Install the [Slack service](https://github.com/keptn-sandbox/slack-service) and configure it to listen for the `sh.keptn.event.notify.triggered` event
- Install the [JIRA Service](https://github.com/keptn-sandbox/jira-service) and configure it to listen for the `sh.keptn.event.report.triggered` event

## Step 4: Trigger Sequence

Your system is set up and ready to go! Just trigger the sequence and Keptn will handle the lifecycle of the tasks for you. Your tooling will respond and your tasks will be achieved.

Check the Keptn's bridge for a full report on how your sequence progressed.

## Summary

It's **very** easy to get started with Keptn. Keptn is designed so that you can provide your own tooling. You decide the best tool for the job and Keptn handles the rest.

Is there a service you'd like to use with Keptn? Join the [Keptn community on Slack](https://slack.keptn.sh) and suggest an integration. I'm on there too - tag me and I'll help out.