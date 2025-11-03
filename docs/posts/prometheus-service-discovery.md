---
title: Prometheus Service Discovery
categories:
- prometheus
date:
  created: 2025-01-10
---

Any realistic usage of Prometheus will have tens, if not hundreds, of scraped endpoints. It becomes impossible to know, track and manage each of these manually.

Thankfully, Prometheus offers a feature called Service Discovery which allows you to delegate the maintenance and discovery of endpoints to a secondary service. In other words, you tell Prometheus to "go over here and get the endpoints from this thing" and it will. No more manual effort involved from you.

This video explains how it all works, with a live demo - of course.

<!-- more -->

<iframe width="560" height="315" src="https://www.youtube.com/embed/wNCuojBXwiM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>