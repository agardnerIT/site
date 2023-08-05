---
layout: post
title: "My First Helm Plugin"
categories: [helm, plugin, development]
header_image: /images/headerimages/helm-logo.png
---

I've just finished creating my first Helm chart and I thought I'd document the process in case it helps others.

## Preparation

This plugin will "wrap" a normal helm command, generate an OpenTelemetry trace and use tracepusher to send it to an OpenTelemetry collector.

You'll need the following installed to follow along:

- [helm](https://helm.sh)
- [git](https://git-scm.com)
- A [tracepusher](https://github.com/agardnerit/releases/latest) binary added to your $PATH

## The Outline

Helm commands usually look like this:

```
helm <command>
```

For example:

```
helm version
```

## What's in a name?

Helm plugins have a name and that name becomes part of the command. In other words, you invoke your plugin during a regular helm command.

If your plugin was called `foo`, you would invoke it like this:

```
helm foo version
```

## What language?

Helm doesn't care what language your plugin is written in. Powershell, shell, Python, Go etc. Helm can run it all.

Of course, you need to know that the end user (the person installing the plugin) has that language available on their machine.

If you write your plugin in Python and the user doesn't have Python? Your plugin will fail.

So what language does every Mac, Linux, Unix have? Plain old bash. That's what we'll write our plugin in today.

## What should it do?

What do you want the plugin to do?

In my case, I want the plugin to:

1. Execute the helm command that the user intended
1. Time the amount of time the command took
1. Call another process that I know is installed on the user machine

I know that this other process is installed because I've listed it in the prerequisites for the plugin.

## The Payload

Create a folder called `trace`. This folder is important. It must match the name of the plugin.

Here's the plugin payload. Save it as a `.sh` file with any name you like. I've called mine `script.sh`

```shell
#!/bin/bash

commandToRun="helm $@"

# If collector env var not set
# default to localhost:4318
if [ -z $HP_OTELCOL_ENDPOINT ]
then
  HP_OTELCOL_ENDPOINT=http://localhost:4318
fi

# Run original helm command
# w/o 'trace' keyword
$commandToRun

duration=$SECONDS

# Use tracepusher to generate an OpenTelemetry trace
# and push it to an OTEL collector 
tracepusher -e $HP_OTELCOL_ENDPOINT -sen helm -spn "$commandToRun" -dur $duration
```

## Explain it!

The first line denotes that this is a bash script.

Then the `commandToRun` is built by using `$@` which, in bash, means "all arguments" and prepending `helm`.

So, the input might be `helm trace install X Y`. In which case, `$@` would be `install X Y`. So now re-add the `helm` command to the beginning. `commandToRun` is now `helm install X Y`.

Next the script checks whether an environment variable `HP_OTELCOL_ENDPOINT` is set. If not, it defaults to `http://localhost:4318`.

Run the command original `helm` command as the user intended (in our example this is `helm install X Y`).

When helm has finished, calculate the amount of seconds this script has been running. The SECONDS variable is [a built-in bash variable](https://man7.org/linux/man-pages/man1/bash.1.html) which provides the number of seconds since the shell was invoked. The script uses this to denote the nubmer of seconds the script has been running.

Finally, the [tracepusher](https://github.com/agardnerit/tracepusher) binary is executed, using the environment variable previously set. Tracepusher will generate an [OpenTelemetry](https://opentelemetry.io) span with a service name of `helm`, a span name identical to the helm command and a duration which matches how long it took to execute the actual helm command.

## Create Helm Plugin

The above gets a running shell script. How do we make that a helm plugin?

Create a new file in the `trace` directory alongside `script.sh` called `plugin.yaml` (again, name is important):

```yaml
name: "trace"
version: "0.1.0"
usage: "helm trace install foo foo/bar"
description: "Generate OpenTelemetry traces for helm commands"
ignoreFlags: false
command: "$HELM_PLUGIN_DIR/script.sh"
platformCommand:
  - os: "linux"
    command: "$HELM_PLUGIN_DIR/script.sh"
hooks:
  install: "chmod +x $HELM_PLUGIN_DIR/script.sh"
```

## Explain it!

The `name` command should be self-explanatory and should match the directory name (and intended plugin name) in this case: `trace`.

The plugin has a `version`. [SemVer](https://semver.org) must be used.

Provide some brief usage instructions in the `usage` field.

`description` is a field for you to give a plugin description.

`ignoreFlags` takes `true` or `false`. If `ignoreFlags` is set to `true`, helm arguments are silently discarded (and thus unavailable to your plugin). For example: `helm version --foo` would become `helm version` with the `--foo` flag being thrown away. Since we want the exact command the user executed, we set this flag to false and thus retain all arguments.

The `command` parameter tells helm what to do when someone runs the plugin. In this case, helm will execute our shell script. `$HELM_PLUGIN_DIR` is an in-built variable that is set by helm itself and always points to the correct plugin directory. Handy!

`platformCommand` allows the plugin author specify different commands based on operating system. Want a shell script for Linux and a Powershell for Windows? That's possible.

Finally, due to Linux's permission requirements, we need the shell script to be executable (have the `x` bit set). So during plugin installation, after `script.sh` is downloaded, `hooks.install` is used to run a `chmod +x` command to ensure the script is executable.

Save `plugin.yaml`

# Install and test locally

If you are in the `trace` folder, you should now have two files:

- `script.sh`
- `plugin.yaml`

Install your plugin by running:

```shell
helm plugin install .
```

If you find a helm plugin online you like, the syntax changes `.` to the URL:

```shell
helm plugin install https://github.com/agardnerit/helm-trace
```

Before you ask, **yes** the repo must be structured like that: `plugin.yaml` at the root.


Back to the locally developed plugin...

You should see:

```
Installed plugin: trace
```

## Try it out

Run a helm command:

```shell
helm trace version
```

If you have an OpenTelemetry collector running on `http://localhost:4318` you should see:

```shell
% helm trace version
version.BuildInfo{Version:"v3.11.2", GitCommit:"912ebc1cd10d38d340f048efaf0abda047c3468e", GitTreeState:"clean", GoVersion:"go1.20.2"}
<Response [200]>
```

If your collector is running elsewhere, set the `HP_OTELCOL_ENDPOINT` then run the command above:

```shell
export HP_OTELCOL_ENDPOINT=http://my.collector.somewhere.com:4318
helm trace version
```

## Summary

So there you have it, your first Helm plugin! There aren't many limitations to what helm and the plugin system can achieve, so go forth and integrate.

Also, please make Helm observable with OpenTelemetry by installing [helm trace](https://github.com/agardnerIT/helm-trace).

## Additional Reading and Links

- The real [helm trace plugin](https://github.com/agardnerIT/helm-trace) (and code)
- [Helm plugin developers guide](https://helm.sh/docs/topics/plugins/)
- [tracepusher](https://github.com/agardnerit/tracepusher)