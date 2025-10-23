---
title: Check your Website for Free using OpenTelemetry
categories:
- opentelemetry
date:
  created: 2025-07-21
---


Here's how to perform basic up/down checks of your websites using the OpenTelemetry Collector.

<!-- more -->

!!! info "Watch"
    If you'd prefer to watch rather than read, I have the following content as a YouTube video:

    [:material-youtube: Free Website Checks using OpenTelemetry](https://youtu.be/Xm7_udnyPx8)

Did you know it is possible to use the OpenTelemetry Collector to perform basic HTTP checks of your webpages?

## Collector Configuration

It's actually really quite easy. For this blog post I'll assume you're already familiar with the collector and its YAML configuration file (if not, I suggest watching the video above as it has a full end-to-end runthrough with no assumptions).

First, you'll need a collector distribution that includes the httpcheck receiver (the contrib and k8s versions both do).

Here's the magic snippet you need:


```
receivers:
  httpcheck:
    collection_interval: 10s
    targets:
      - endpoint: http://example.com
        method: GET
      - endpoint: https://agardner.net
        method: GET
      ...
exporters:
  debug:
    verbosity: detailed
  otlphttp:
     endpoint: ...

service:
  pipelines:
    metrics:
      receivers: [httpcheck]
      exporters: [otlphttp, debug etc...]
```

The `collection_interval` defines how often the collector will check each endpoint. Note: 10 seconds is far too frequent for production. Probably once a minute is good enough (`1m`).

That's it, start the collector and as long as you've configured the `exporters` section correctly for your backend, you should see metrics in your Observability tool.
How Green is your Observability? How the OpenTelemetry collector can help