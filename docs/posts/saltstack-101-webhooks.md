---
layout: post
title: Saltstack 101 - Webhooks
header_image: /images/headerimages/saltstack-setup-configuration-header.png
categories:
- automation
- devops
- salt
- saltstack
- tutorial
date:
  created: 2018-04-05
---

Control Saltstack remotely via HTTP(S) webhooks and automate your IT infrastructure...

<!-- more -->

## Prerequisites

If you’ve followed the [previous tutorial](saltstack-101-setup-configuration.md) you will have a working salt master and minion machine which can successfully talk to each other. I highly recommend you review the previous tutorial before continuing.

While following this tutorial you have two choices:

- Use a domain name with a proper (not self signed) SSL certificate (recommended approach).
- Setup the system in unsecured HTTP mode (easier, but obviously less secure).

We will be using [LetsEncrypt](https://letsencrypt.org/) to issue a free SSL certificate and since domain names are cheap, I recommend you get one too.

There are a number of sites offering free domain names available. I’ve never used any of these services so I’m not willing to vouch for them.

## Scenario

In this tutorial, we will:

- Install an Apache server on the `minion`. This will mimic the customer’s webserver.
- Create an HTTP endpoint on the salt `master`. This will act as a webhook to receive POST values.
- Control the `minion` remotely via webhooks.
- Demonstrate the webhook functionality by remotely starting and stopping the apache server.

## Point Domain to Master

If using your own domain, make sure it’s pointing at your master now.

## Install Customer Web Server
INSTALL CUSTOMER WEB SERVER

Install apache2 on the minion.

Remember this apache2 will not be served your domain, but will be accessible via the minion’s IP address.

From the master, run: `salt 'saltstack-minion' pkg.install apache2`

Check that it’s up and running. You should see the default Apache page.

## Install Salt API on Master

The `salt-api` package allows remote connections to the salt master.

On the master run: `sudo apt-get install salt-api -y`

Ensure outputs of both `salt-api --version` and `salt --version` match (on the master):

```bash
root@saltstack-master:~# salt-api --version
  salt-api 2018.3.0 (Oxygen)
root@saltstack-master:~# salt --version
  salt 2018.3.0 (Oxygen)
```

## Create REST User

This user will be used to authenticate while using the REST interface. On the master:

```bash
sudo useradd demouser
sudo passwd demouser
GRANT REST USER PERMISSIONS
```

Now give your `demouser` permissions to access all saltstack functions.

On the master: `nano /etc/salt/master`

Search for `external_auth` and uncomment the template to give your demouser permissions.

Your code should look like this:

```
external_auth:
  pam:
    demouser:
      - .*
```

## Install CherryPy

This is a python webserver which will give us our webhook endpoints
First, we need the `python3-setuptools` package as it’s used by cherrypy.

```bash
# Install pip and the setuptools package as it's used by cherrypy
sudo apt-get install python-pip python3-setuptools -y
# Now install cherrypy
sudo pip install cherrypy
# Make sure cherrypy is up to date
sudo pip install --upgrade cherrypy
```

## Create SSL Certificate

If you’re using HTTP, skip this step. Install the LetsEncrypt certbot and generate your SSL certificates.
Replace `example.com` and `www.example.com` with your domain names.

Run the following on the master:

```bash
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update
sudo apt-get install certbot -y
sudo certbot certonly --standalone --agree-tos --email me@example.com -n -d example.com -d www.example.com
```

Certs will be stored in:

```bash
/etc/letsencrypt/live/example.com/fullchain.pem
/etc/letsencrypt/live/example.com/privkey.pem
```

## Add CherryPy Configuration to Master

Add the following configuration (altering as appropriate) to the end of your `/etc/salt/master` config file.

```
nano /etc/salt/master
```

Then add this:

```
rest_cherrypy:
  port: 8000
  # Uncomment following line only if you're running without a domain name and in HTTP mode.
  #disable_ssl: True
  # Uncomment following lines if using custom domain with LetsEncrypt
  #ssl_crt: /etc/letsencrypt/live/example.com/fullchain.pem
  #ssl_key: /etc/letsencrypt/live/example.com/privkey.pem
```

## Restart Salt Master and Salt API

```bash
sudo service salt-master stop && sudo service salt-api stop
sudo service salt-master start && sudo service salt-api start
```

## You've Come A Long Way Baby...

If you’re here you should be able to access the master on port `8000` (either via HTTPS with your domain or HTTP with an IP address). Either way, you should have no SSL certificate warnings.

You’ll get a `200 OK` response and this text:

```json
{"clients": ["local", "local_async", "local_batch", "local_subset", "runner", "runner_async", "ssh", "wheel", "wheel_async"], "return": "Welcome"}
```

## Retrieve Your Auth Token

In order to use the REST endpoints, we need to authenticate. The portable authentication module (`pam`) makes this easy.

Login once with your username and password and you’ll receive a token

```
POST https://DOMAIN-OR-MASTER-IP:8000/login
Headers:
  Content-Type: application/json

Body:
{
  "username": "demouser",
  "password": "password",
  "eauth": "pam"
}
```

Copy the token value from the returned content and include it in the `X-Auth-Token` header.

## Ping Minions Via REST

```
POST https://DOMAIN-OR-MASTER-IP:8000
Headers:
  X-Auth-Token: token value from above...

Request Body:
{
  "client": "local",
  "tgt": "*",
  "fun": "test.ping"
}
```

_fun meaning function, not fun and frivolity :)_

If successful, you should see this content returned:

```json
{
"return": [
    {
        "saltstack-minion": true
    }
  ]
}
```

Congratulations. Your ping test was successful and you can now successfully control your infrastructure via webhooks and REST calls. How very DevOps of you!