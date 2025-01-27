---

title: Dynatrace OneAgent - Same Binary, Different Tenants
header_image: /images/headerimages/oneagent-same-binary-different-tenants-header.png
categories:
- backup
- restore
- tutorial
- wordpress
- digitalocean
date:
  created: 2018-03-30
---

Can we use the same Dynatrace OneAgent installer in two different environments? That was the question posed by a customer recently.

Let’s see how it’s done...

<!-- more -->

## Prerequisites

- A Dynatrace account. Sign up for a [free 15 day trial here](https://dynatrace.com/trial).

## Why?

By default, the OneAgent installer you download from your tenant is predefined to point to that tenant. In most cases this works perfectly and is the best way to install the OneAgent (lowest effort).

However, your organisational policy or workflow may demand that you use the same OneAgent installer for two (or more tenants). One example is using the same binary in a pipeline where the OneAgent will point at a preproduction tenant or a production tenant.

## How?

The default OneAgent install commands look like this:

```bash
wget -O Dynatrace-OneAgent-Linux-VERSION.sh "https://abc123.live.dynatrace.com/api/v1/deployment/installer/agent/unix/default/latest?Api-Token=def456&amp;arch=x86&amp;flavor=default
sudo /bin/sh Dynatrace-OneAgent-Linux-VERSION.sh APP_LOG_CONTENT_ACCESS=1
```

To reconfigure the OneAgent, there are 3 additional (mandatory) parameters to pass during the install.
`SERVER`, `TENANT` and `TENANT_TOKEN`.

- The `SERVER` variable is the full URL to the tenant eg. `https://abc123.live.dynatrace.com`
- The `TENANT` variable is the tenant part of the URL eg. `abc123`
- The `TENANT_TOKEN` is a variable which should be considered secret and private. Encrypt as you would with any other password.

## Retrieve Your TENANT_TOKEN

A REST call is necessary to retrieve your `TENANT_TOKEN`.

`GET https://TENANT.live.dynatrace.com/api/v1/deployment/installer/agent/connectioninfo?Api-Token=YOURAPITOKEN`

The `Api-Token` needs to have `InstallerDownload` permission.

To generate one, go to Settings > Integration > Platform as a Service

## Put It All Together

So, assuming the following:

```
SERVER=https://abc123.live.dynatrace.com
TENANT=abc123
TENANT_TOKEN=9876hjk
```

All you need to do is append them to the installer line:

```bash
wget -O Dynatrace-OneAgent-Linux-VERSION.sh "https://abc123.live.dynatrace.com/api/v1/deployment/installer/agent/unix/default/latest?Api-Token=def456&amp;arch=x86&amp;flavor=default
sudo /bin/sh Dynatrace-OneAgent-Linux-VERSION.sh SERVER=https://abc123.live.dynatrace.com TENANT=abc123 TENANT_TOKEN=9876hjk APP_LOG_CONTENT_ACCESS=1
```
