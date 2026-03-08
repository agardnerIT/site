---
title: Automatically instrument everything. Hands on with the OpenTelemetry injector
categories:
- opentelemetry
date:
  created: 2026-02-25
---


In this video I demonstrate the new OpenTelemetry injector. It's a mechanism to automatically inject OTEL into your code with zero code or startup script changes. It's potentially a great way to gain Observability of non Kubernetes workloads like VMs.

<!-- more -->

It leverages `LD_PRELOAD`. You add the `LD_PRELOAD` instruction to your VM at startup and the rest happens automatically.

Do heed the warnings towards the end of the video though since it's still early days for this tool!

GitHub Repo: [https://github.com/agardnerIT/opentelemetry-injector-tutorial](https://github.com/agardnerIT/opentelemetry-injector-tutorial)

<iframe width="560" height="315" src="https://www.youtube.com/embed/AFHbhcciASQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>