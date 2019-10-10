---
layout: post
title: Ansible 101 - Playbooks
categories: [ansible, automation, devops]
---

In the [previous tutorial](/ansible-101-basics) we covered Ansible setup and some basic ad-hoc commands. It’s time to get organised and introduce the ability to easily repeat ourselves consistently. This tutorial will focus on playbooks...

## Overview

Ansible playbooks are a way to define orchestration, configuration management and settings in an easy to read format. This also means that they can be easily stored in a version control system (such as Git) or shared amongst coworkers.

## An Example Playbook
AN EXAMPLE PLAYBOOK

First, assume that our `/etc/ansible/hosts` file looks like this:

```
[webservers]
10.0.0.2
10.0.0.3

[payment-service]
10.0.0.4
10.0.0.5
10.0.0.6

[database]
10.0.0.7
10.0.0.8
```
See if you can guess what this playbook does and to which machines. Ansible really is that simple. Scroll down for the full explanation in case you’re stuck.

```yaml
---
- hosts: webservers
  become: true

  tasks:

  - name: Install apache2 webserver
    package:
      name: apache2
      state: latest

  - name: Ensure apache2 is started
    service:
      name: apache2
      state: started
```

In case you hadn’t guessed, let’s walk through that playbook and explain:

- A playbook executes top down, in order.
- We specify the hosts that will be affected by this playbook. Our webservers group (`10.0.0.2` and `10.0.0.3`).
- We specify that ansible can `become` another user. By default this means that the script will `sudo` to "become" `root`.
- We specify a task. The `name` of the task is purely for us humans. The first task uses the `package` module to install latest available version of the `apache2` module.
- The next task uses the `service` module to ensure that `apache2` is started.

Notice something too, we installed `apache2` to two webservers with a single playbook. Even if our infrastructure scaled up to hundreds of thousands of webservers – all we’d need to do is add new IP addresses to our host file. Simple!

## Indentation & Idempotence

Indentation is extremely important to ansible because it uses the YAML format. Check your playbooks by adding the `--syntax-check` flag (eg. `ansible-playbook ~/myPlaybook.yml --syntax-check`)

**Idempotence** is a key concept in Ansible. If something is idempotent it means the same operation can be executed multiple times without (necessarily) changing the result.

What this means in terms of Ansible is that the same playbook should be able to be executed multiple times without necessarily affecting the result.

Think about that for a second. It’s extremely powerful. It means you can write a playbook to define the state of your infrastructure then run it continuously (say in a `cron` job). Ansible will ensure that your infrastructure is always in your desired state. If anything changes, Ansible will fix it for you.

Take the example above. We could run that playbook every 30 seconds. In essence, Ansible first checks whether `apache2` is installed. If it is, Ansible knows not to do anything. Ansible then checks whether `apache2` is running. If it is, Ansible does nothing. In other words, if everything is running as it should, nothing will happen (as, by definition, nothing needs to happen). After all, you wouldn’t want your web servers being re-installed and restarted every 30 seconds, would you!?