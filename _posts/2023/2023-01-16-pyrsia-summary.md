---
layout: post
title: "Hands on with Pyrsia in under 5 minutes: Video Summary"
categories: [continuous delivery foundation, cdfoundation, pyrsia, summary]
header_image: /images/headerimages/pyrsia-header.svg
---

This is a text-based version of [this video](https://youtu.be/lZI_waRi1K0) so if you prefer reading to watching, read on!

Want to jump straight to the [Pyrsia hands-on](http://killercoda.com/agardnerit/scenario/pyrsia)? 

# Pyrsia: Decentralized Package Network
[Pyrsia](https://pyrsia.io) is the newest CDFoundation project.

# What is Pyrsia?
Pyrsia is a decentralized package network. Independant build nodes individually build open source software package (at the time of writing, Docker images and Maven packages).

Each build node in the network commits the build results to a blockchain and only when consensus is reached, will the artifact be available on the network.

This design ensures that images are what they promise to be and no one actor can compromise the network - because all build nodes need to agree. If one build node was to be compromised and commit a different set of metadata to the blockchain, the network would reject the build.

This blockchain (immutable ledger) and consensus approach promises a step up in security for those relying on open source software and hopefully will minimise software supply chain risks.

All actions are committed to the Pyrsia transparency log - which any Pyrsia user can inspect at any time.

# Pyrsia Hands On
During the [Pyrsia hands-on](http://killercoda.com/agardnerit/scenario/pyrsia) exercise, you will install Pyrsia, connect to the network and pull an image from the network.

You will then retrieve the transparency log for that image to see how the network came to a consensus about that image.

# New Project Each Week
Each week in 2023 I will pick a new open source project to review. The entire list is [here](https://agardner.net/project-intros).

The series is designed to be interactive - if you have a project you'd like me to review - please do [get in contact](https://agardner.net/contact) and suggest a project!

I hope you enjoy the Pyrsia project!