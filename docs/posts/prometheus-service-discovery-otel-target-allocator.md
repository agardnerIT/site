---
title: Prometheus Service Discovery and OpenTelemetry Target Allocator
categories:
- opentelemetry
- prometheus
date:
  created: 2025-07-30
---

In this post & video I'll explain how to get metrics from a Kubernetes cluster the easy way. Starting with service discovery and `http_sd_config` then using the OpenTelemetry Target Allocator.

<!-- more -->

Here's how to get Prometheus metrics from your Kubernetes applications easily. First I show the "basic" way for a single cluster using the service discovery mechanisms in the OpenTelemetry collector http_sd_config.

Then I extend the usecase to cover a more realistic multi-cluster, production ready setup using the OpenTelemetry Operator and Target Allocator.

GitHub repo: [https://github.com/agardnerIT/k8s-target-allocator](https://github.com/agardnerIT/k8s-target-allocator)

[:material-youtube: CrewAI Observability](https://youtu.be/)
<iframe width="560" height="315" src="https://www.youtube.com/embed/Jc7sltedVpo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>