---

title: "AppMon 7 \u2013 Automated User Data Scripts"
header_image: /images/headerimages/user-data-header.jpg
categories:
- appmon
- automation
- aws
date:
  created: 2017-07-22
---

--8<-- "docs/snippets/warning-legacy-dynatrace.md"

I often find myself needing to quickly create AppMon setups in AWS for POCs and demos, so I built myself a big green go button in the form of some user data scripts.

<!-- more -->

Yes, Dynatrace offers Ansible, Chef and Puppet scripts for longer term / more robust configurations, but I just want something up and running quickly with fewer dependencies.

## Server User Data Script

Note the sizing and memory settings on lines #12 and #13 – you’ll want to set these correctly to your environment.

https://gist.github.com/agardnerIT/71623c9e47b178ede8c1b8e810d70117

## Collector User Data Script

You’ll need to specify the server IP address on line #12. Also note that this sets the RAM to 512MB which is too small for real-world use and this script should **only** be used in demo scenarios.

This script also presets the collector group (making OOTB resilience possible) and the collector name (otherwise it’ll pick up the AWS IP as the name eg. ip-172-10-12-12).

https://gist.github.com/agardnerIT/9ece2319d8c354fff02c03572077c002

## Apache with Webserver Agent

This script creates an Apache web server with the AppMon agent preinstalled. You’ll need to create an agent group for this agent and set the relevant name on line #16. You’ll also need to specify the collector IP / DNS on line #17.

https://gist.github.com/agardnerIT/c7a83f447e0778f0034e2f4f04424226

I hope you find these useful for quickly getting things up and running. Are there any other components you’d like to see user data scripts for? Let me know and I’ll create them.
