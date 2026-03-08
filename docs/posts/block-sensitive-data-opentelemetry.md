---
title: Block API Tokens and Sensitive Data using the OpenTelemetry Collector
categories:
- opentelemetry
- collector
- security
date:
  created: 2026-02-16
---


In this video I use mazen160's fantastic secrets regex list to build filter and transform processors rules for the OpenTelemetry collector. This configuration blocks 883 different API tokens, keys and sensitive strings from ever reaching your observability backend systems.

<!-- more -->

Thanks to mazen160's repo: https://github.com/mazen160/secrets-patterns-db

The code for this video is here: https://github.com/agardnerIT/secret-patterns-db-otel-collector

<iframe width="560" height="315" src="https://www.youtube.com/embed/f7Zx6qzLiVY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>