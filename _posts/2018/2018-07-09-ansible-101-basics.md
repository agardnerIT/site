---
layout: post
title: Ansible 101 - The Basics
categories: [ansible, automation, devops]
---

Ansible is an automation and configuration management system. It is incredibly simple to get going and extremely powerful once mastered. The first part in the series aims to get you up and running with Ansible…

## Overview

This is part one of the series, in this post I’ll outline what Ansible is, get Ansible installed, get you setup and run the first few commands to give you a taste of how powerful Ansible can be.

Ansible runs on a `control` machine which is where we’ll write and store all our Ansible code. It’s also where we’ll trigger all the Ansible executions. The `target machine(s)` do not need anything installed on them.

The control machine must be linux, unix or MacOS. Not Windows.

I’ll be using MacOS for my control machine but you can easily use Ubuntu Desktop running in a VM (I recommend VirtualBox).

STEP 1: SETUP TARGET MACHINE

The Ansible control machine communicates with the target machines via SSH. So spin up a VM and make sure you can ping from your host to your target machine.

My target IP is `192.168.43.237` and I can successfully ping it from my host:

```bash
adam@ubuntu $ ifconfig
    inet 192.168.43.237...
```

Note: My `control` machine username is `adamgardner`. My `target` machine username is `adam`.

Next, create an SSH key and copy it to the target machine:

```bash
# Generate SSH key. Use all default values. I chose not to password protect it
ssh-keygen -t rsa -b 4096

# Copy the SSH key to the target machine. Repeat if you have multiple targets
ssh-copy-id TARGET-MACHINE-ID 
```

Now ensure you can SSH from the control to the target machine:

```bash
ssh 192.168.43.237 -l adam
...
Adams-MBP: - adamgardner $ ssh 192.168.43.237 -l adam
...
Welcome to Ubuntu 18.04...
adam@ubuntu $
```

## Step 2: Install Ansible

Now that we have the groundwork covered, it’s time to install Ansible and run our first command to let Ansible ping our node(s).

Installing Ansible varies depending on what OS your control machine is running. Since I recommended Ubuntu, here are the Ubuntu and MacOS instructions:

**Ubuntu**

```bash
sudo apt-get update -y
sudo apt-get install software-properties-common -y
sudo apt-add-repository ppa:ansible/ansible -y
sudo apt-get update -y
sudo apt-get install ansible -y
```

**MacOS**

```bash
sudo easy_install pip
sudo pip install ansible
```

Now double check that Ansible has installed correctly by retrieving it’s version number:

```bash
ansible --version
```

## Tell Control Machine About Target(s)

Amsible uses a push methodology. This means that commands are propogated out from the control machine to each target machine. Therefore it makes sense that the control machine must know the location of each target machine.

Ansible uses a `hosts` file to achieve this. The hostname or IP of each target is listed in this special file. This hosts file needs to live at `/etc/ansible/hosts` so first, ensure the folder structure exists and if needed, create that file.

Let’s add our target machine (IP: `192.168.43.237`) to the hosts file.

```
sudo nano /etc/ansible/hosts
```

![]({{ site.baseurl }}/images/postimages/ansible-basics-1.png)

Note the two additional parameters: `ansible_user` denotes the username I wish to use when connecting to this target host (recall that the username of my VM was `adam`).

I’ve included `ansible_python_intepreter` because Ansible runs the python interpreter at `/usr/bin/python` but my setup has python 3 installed which lives at `/usr/bin/python3`.

Now that we’ve defined our target(s), we can use the Ansible `ping` module to ping all target nodes:

```
ansible -m ping all
```

Let’s do something more useful. Let’s create a file on each target host. We’ll use the [file module](https://docs.ansible.com/ansible/latest/modules/file_module.html) and pass a couple of arguments. Namely, the `path` of the file to create and the desired `state` of the file.

```
ansible -m file --args 'path=/tmp/test.txt state=touch'
```

## Conclusion

Congratulations. If you’ve made it this far, you’re should already be starting to see the potential Ansible gives for automation, repeatability and easy configuration management. Part two of the series will delve deeper into Ansible commands with some real-world demos and introduce the concept of Playbooks and Idempotence.