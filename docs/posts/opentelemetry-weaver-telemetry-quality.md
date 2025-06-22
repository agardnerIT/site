---
title: Judging Telemetry Quality using Weaver
categories:
- opentelemetry
- weaver
date:
  created: 2025-06-22
---

"Is my telemetry good?" In this post I'll show you how to answer that question using the Weaver tool from the OpenTelemetry project.

<!-- more -->

!!! info "Watch"
    If you'd prefer to watch rather than read, I have the following content as a YouTube video:

    [:material-youtube: Judging Telemetry Quality using OpenTelemetry Weaver](https://youtu.be/ReZzjR8Anrs)

## Overview

I regularly get asked a variation of: "is my telemetry any good?" and "what can we do to improve our telemetry data to better assist us during incidents?"

Assuming the asked actually _has_ the correct telemetry to assist them, then what these questions usually boil down to, is the fact that their telemetry does not carry the correct amount of metadata.

When telemetry signals (metrics, logs, events, traces, profiles etc.) are used during an incident, you need to quickly identify the issue, who is affected, who those entities belong to and thus you can quickly notify and begin the remediation process.

## So What is "the right metadata"?

Easy to say, harder to achieve, right? Defining standards across an organisation is hard - doing so across multiple organisations is even harder.

Well, a great place to start are semantic conventions. These are agreed-upon standards that define what metadata is included on the signals. Semantic conventions usually use the words `MUST`, `SHOULD` and `COULD` to indicate how important each piece of metadata is and thus how important

Let's make this more concrete: The [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/) defines attributes for all kinds of things - from how to provide a host name (`Recommended` with `host.name`) to how to indicate the type of database(eg. `redis`) (`Required` with `db.system.name`).

The OpenTelemetry semantic conventions even tell us _how_ to report certain metrics. For example, if you and I both wanted to report CPU usage, we MUST use [http.server.request.duration](https://opentelemetry.io/docs/specs/semconv/http/http-metrics/#metric-httpserverrequestduration) and report a histogram.

At first glance this seems like uneccessary control and overhead, but this kind of standardisation pays dividends at scale because the backend system (wherever we send telemetry data) can now understand our signals as like-for-like and this know that it can treat things equivalently.

This standardisation is also the key to answering our question: How good is our telemetry?

## Roll Your Own Semantic Convention?

Your first instinct might be to develop your own in-house convention. However I would caution against that, for a few reasons:

1. It is not usually required - a lot of thought (and expertise from across the industry) has gone into the OpenTelemetry SemConv.
1. Third party suppliers, SaaS vendors you rely upon, and others won't be following your in-house semantic conventions. Meaning you're creating downstrea work to "map" one metric to another.
1. Following the standard can be a sales tool. If you supply metrics for another entity to consume, you're creating work for them as they need to map your custom "stuff" to their "stuff". If I was evaluating vendors and was given the choice between two equal products - one which followed a widely adopted standard and one which "rolled their own" - I'd pick the standard-following one every time.

Defining an in-house standard can be appropriate - if you're doing something _so incredibly specialised_ that no other company is doing it. Let's be honest though, you're probably not (and even if you were, you should submit it to the OpenTelemetry spec, make a lot of noise about it and use it as a marketing / PR activity that you're a thought leader).

All of that said, the Weaver tool we'll use below _can_ work with your custom telemetry spec, if you still choose to go down this path.

## Semantic Conventions Aid Quality Judgments

Now that there's a way of defining things against a standard (OpenTelemetry, an in-house one or both) the question can now legitimately be asked: Is my telemetry any good?

!!! tip
    All you need to do is find out "how far away" from fully meeting the specifications you are.
    
    * If the telemetry is a 100% match, then yes, your telemetry is perfect
    * If you are only barely matching the agreed-upon rules, your telemetry has room for improvement

## Weaver

As you've probably guessed by now, Weaver, from the OpenTelemetry project, is tool which allows you to evaluate your live realtime telemetry against the semantic conventions you choose.

Weaver acts as an endpoint. Telemetry is sent to Weaver and Weaver produces an output report.

### Step 1: Start Weaver

Start Weaver, informing it to wait for `60` seconds without receiving telemetry before shutting down. The command below also sets the output format to `JSON`, creates a new folder called `weaver-output` and saves a new file in there called `live_check.json` when Weaver closes.

* Port `4317` is used to receive telemetry data (on the gRPC port).
* Port `4320` is optional and should be included if you wish to stop Weaver via the `curl` command (see later).

!!! info "Weaver Binary"
    There is also a [standalone Weaver binary available on GitHub](https://github.com/open-telemetry/weaver/releases)

```shell
docker run --rm \
  -p 4317:4317 \
  -p 4320:4320 \
  -u $(id -u ${USER}):$(id -g ${USER}) \
  --env HOME=/tmp/weaver \
  otel/weaver:v0.15.2 registry live-check \
  --inactivity-timeout=60 \
  --output=weaver-output \
  --format=json
```

or (for standalone binary):

```shell
./weaver registry live-check \
  --inactivity-timeout=60 \
  --output=weaver-output \
  --format=json
```

!!! info
    Notice that when Weaver starts, it defaults to reading the OpenTelemetry semantic convention:

    ```
    Weaver Registry Live Check
    Resolving registry `https://github.com/open-telemetry/semantic-conventions.git[model]`
    ```

You'll know Weaver is ready when you see:

```
The OTLP receiver will stop after 60 seconds of inactivity.
```

### Step 3: Send a Trace

Use docker / podman and the OpenTelemetry [telemetrygen](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/cmd/telemetrygen/README.md) tool to send a single trace to Weaver.

The command sends the trace to the special `host.docker.internal` address (which means `localhost` on the host machine where docker is running). The `--otlp-insecure` flag is also set because Weaver is listening insecurely (that's OK because this is test data + we're on localhost).

```shell
docker run --rm \
  ghcr.io/open-telemetry/opentelemetry-collector-contrib/telemetrygen:v0.128.0 \
  traces --traces=1 \
  --otlp-insecure=true \
  --otlp-endpoint=host.docker.internal:4317
```

The container will run and exit. If it works, the last message should be:

```
INFO    traces/traces.go:64  stopping the exporter
```

### Step 4: Stop Weaver

Stop Weaver either by pressing `Ctrl + C` or sending a `curl` command to the `/stop` endpoint of Weaver:

```
curl -X POST http://localhost:4320/stop
```

### Step 5: Inspect Weaver Output Report

Open `weaver-output/live_check.json` and inspect the output report.

In this report Weaver has checked `8` entities: `1` resource, `2` spans and `5` attributes. It has found `6` advisories.

```json
...
"total_advisories": 6,
"total_entities": 8,
"total_entities_by_type": {
  "attribute": 5,
  "resource": 1,
  "span": 2
}
...
```

Scrolling back up, each "thing" gets an array of `all_advice` given for that "thing". For example, here's the output for `1` of the span attributes.

Weaver has identified one `violation` and one `improvement` and thus, for this span attribute, the `highest_advice_level` (ie. the worst thing about it) is a `voilation`.

```
{
  "live_check_result": {
    "all_advice": [
      {
        "advice_level": "violation",
        "advice_type": "deprecated",
        "message": "Replaced by `network.peer.address`.",
        "value": "renamed"
      },
      {
        "advice_level": "improvement",
        "advice_type": "stability",
        "message": "Is not stable",
        "value": "development"
      }
    ],
  "highest_advice_level": "violation"
},
"name": "net.sock.peer.addr",
"type": "string",
"value": "1.2.3.4"
}
```

There are so many more statistics that Weaver produces and this is a gold-mine for things like preventing CICD pipelines from progressing if telemetry is not "good enough".

!!! info "Watch this in action"
    If you want to see this in action, check out [this YouTube video](https://youtu.be/ReZzjR8Anrs).

## Summary

In this post you've discovered how Weaver, a tool from the OpenTelemetry project, can help you to understand the realtime quality of your telemetry data against semantic conventions.

Weaver is a new tool and there is a lot more it can do. I'm only just starting to learn it now, so stay tuned and I'll bring you more when I understand more about it. It certainly seems very useful for DevOps / SRE folk!