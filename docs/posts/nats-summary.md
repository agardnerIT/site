---

title: 'Hands on with NATS in under 4 minutes: Video Summary'
categories:
- cncf
- nats
- summary
header_image: /images/headerimages/nats-header.png
date:
  created: 2023-01-06
---

This is a text-based version of [this video](https://www.youtube.com/watch?v=CWxnb4ap1Z4) so if you prefer reading to watching, read on!

<!-- more -->

Want to jump straight to the [NATS hands-on](http://killercoda.com/agardnerit/scenario/nats)? 

# NATS: A CNCF Incubating Project
[NATS](https://nats.io) is a cloud native Computing Foundation (or CNCF incubating project). An incubating project is the middle of three tiers (sandbox, incubating and graduated).

Incubating projects have a an established security protocol, commits or contributions from a variety of people and not just one person, project or company. All of that means that NATS (or incubating projects in general) should have a fairly stable life and should not just dissapear overnight - meaning they should be safe to adopt.

# What is NATS?
NATS describes itself as message oriented middleware. Two computer systems (A & B) need to send data to one another.

Nat sits in the middle and enables that communication it does so based on subjects.

A "publisher" will publish a message to a particular subject and then one or more systems can listen to that subject and receive all data destined for them.

# NATS Hands On
During the [NATS hands-on](http://killercoda.com/agardnerit/scenario/nats) exercise, NATS will be installed on a Kubernetes cluster.

You will then publish a message to a `test` subject and another consumer will listen for messages on that `test` subject. You will then create two new subjects: `names.dog` and `names.cat` and publish a
message on `names.dog` to show that none of the other consumers receive that message there's only one person receiving that message.

# New Project Each Week
Each week in 2023 I will pick a new open source project to review. The entire list is [here](https://agardner.net/project-intros).

The series is designed to be interactive - if you have a project you'd like me to review - please do [get in contact](https://agardner.net/contact) and suggest a project!

I hope you enjoy the NATS project!