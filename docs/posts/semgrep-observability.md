---
title: Observability of Semgrep output using the OpenTelemetry Collector
categories:
- opentelemetry
- security
- static code analysis
date:
  created: 2026-03-08
---


This video demonstrates how to process and parse [semgrep](https://github.com/semgrep/semgrep) output using the OpenTelemetry Collector. First the JSON reports are saved to disk, read by the collector and parsed. Then we dynamically enrich the report with new key value pairs, drop log attributes to save money and finally create metrics from the log JSON data.

<!-- more -->

<iframe width="560" height="315" src="https://www.youtube.com/embed/lPQprZUYNZQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>