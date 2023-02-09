---
layout: post
title: "Dive: Explore and Optimise your Container Images"
categories: [dive, containers, summary]
header_image: /images/headerimages/dive-header.png
---

This is a text-based version of [this video](https://www.youtube.com/watch?v=giKfx2ScfHM) so if you prefer reading to watching, read on!

Want to jump straight to the [Dive hands-on](http://killercoda.com/agardnerit/scenario/dive)? 

# Thank you to @dnsmichi
Thank you to [@dnsmichi](https://dnsmichi.at) for posting about this tool. Go give him a follow on Masterdon, LinkedIn or your platform of choice.

* Apologies about the pronounciation. It's "mee-ch-ee" "free-dree-ck" - so I got that wrong within 30 seconds. Sorry!

# The Dive Tool
[Dive](https://github.com/wagoodman/dive) is a tool for exploring and optimising your OCI container images (works with Docker too).

The tool will, layer by layer, analyse a given image and provide a report of where the space is used and thus potentially what you could remove to make it smaller.

Shrinking images has many advantages:

- Faster build times
- Faster download and startup times
- Lower storage cost
- Potentially a more secure image (anything *not* in the image is one less thing that can be become vulnerable and hacked)

# Thresholds
[Dive](https://github.com/wagoodman/dive) can also be executed in `ci` mode whereby you provide some acceptable thresholds and the result will be a failure if those numbers aren't met. In this way, you can use Dive as a basic quality gate in your build process to prevent large images from creeping into production.

# Dive Hands On
If this sounds good, [go and get hands-on with Dive](https://killercoda.com/agardnerit/scenario/dive) in your browser with nothing to install - then check out the [official repository](https://github.com/wagoodman/dive).

# New Project Each Week
Each week in 2023 I will pick a new open source project to review. The entire list is [here](https://agardner.net/project-intros).

The series is designed to be interactive - if you have a project you'd like me to review - please do [get in contact](https://agardner.net/contact) and suggest a project!

I hope you enjoy Dive!