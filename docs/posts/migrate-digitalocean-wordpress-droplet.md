---

title: Migrate a DigitalOcean Wordpress Droplet in Under 5 Minutes
header_image: /images/headerimages/migrate-wordpress-header.png
categories:
- backup
- restore
- tutorial
- wordpress
- digitalocean
date:
  created: 2018-03-24
---

This tutorial will guide you through how to backup, rebuild a DigitalOcean droplet, setup SSL encryption and restore a WordPress site in under 5 minutes...

<!-- more -->

## Prerequisites

- A DigitalOcean account (obviously) (Run WordPress free for 2 months with [this link](https://m.do.co/c/fdf58b08514e).

## Assumptions

- An existing droplet running a OneClick wordpress instance.
- You’ve used Let’s Encrypt to enable SSL.

## Let's Get To It

- Login to your wp-admin and install the “UpdraftPlus – Backup/Restore” plugin.
- In admin section, go to Settings > UpdraftPlus Backups
- Click Backup now then flick to the Existing Backups tab and download the 5 files it provides (Database, Plugins, Themes, Uploads, Others).
- Spin up a new OneClick droplet.
- SSH into the new box to activate WordPress.
- In the DigitalOcean Control Panel, go to Networking and point your Networking to the new droplet.
- Back in the new droplet SSH session, add a new non-root user with sudo permissions:

```bash
adduser USERNAME
# Enter Password
usermod -aG sudo USERNAME
su - USERNAME
mkdir ~/.ssh/
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Paste in your public SSH Key
chmod 600 ~/.ssh/authorized_keys
exit
```

## Set Up Let's Encrypt SSL

Still in the new droplet SSH session, run the following commands:

```bash
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-apache
sudo certbot --apache -d YOURDOMAIN.com -d www.YOURDOMAIN.com
# Enter an email address
# First option is "a"
# Secnd option is "n"
# Third option is "2"
# Fourth option is "2"
```

## Test SSL Renewal

`sudo certbot renew --dry-run`

Let’s Encrypt certificates run out after 90 days but don’t worry – certbot takes care of auto-renewal for you. Nothing else to worry about here.

You’ve now got valid SSL for free, forever.

## Setup & Restore Wordpress

- Go to your domain and setup wordpress. Notice that you’re automatically using HTTPS.
- Enter a new temporary admin user / password here. It’ll be overwritten soon.
- Once setup, login to your wp-admin section (with the admin details you set above).
- Install the “UpdraftPlus – Backup/Restore” plugin and activate it.
- Go to Settings > UpdraftPlus Backups and click Restore.
- Upload the 5 files you saved to your computer at the beginning of this tutorial.
- Follow the wizard to restore your site (and users) so now you’re back to your ORIGINAL usernames and passwords. You can discard the temporary admin account details.