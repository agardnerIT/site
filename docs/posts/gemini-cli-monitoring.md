---
title: How to monitor Google's Gemini CLI using OpenTelemetry
categories:
- opentelemetry
- tracing
- ai
- gemini
date:
  created: 2025-10-27
---

Track token counts, model usage, tool usage and "developer idle time" (the time you sit waiting for an answer when using Google's Gemini CLI and the OpenTelemetry collector. In this video, I show you how...

<!-- more -->

I configure the Gemini CLI to send metrics and logs. I spin up the OpenTelemetry collector to receive that telemetry and I leverage OpenObserve as the backend to visualise the data.

Now you can have full, runtime and realtime usage statistics of your Gemini CLI token usage split by model, tool usage and perhaps most importantly, you can track your "idle time".

<iframe width="560" height="315" src="https://www.youtube.com/embed/00je5u_N1j8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>