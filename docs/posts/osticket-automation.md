---
layout: post
title: osTicket Automated Install Script
header_image: /images/headerimages/osticket.png
categories:
- osticket
- automation
- shell script
date:
  created: 2020-03-09
---

[osTicket](https://github.com/osticket/osticket) is one of the leading open source ticketing systems. Here's an easy way to spin up an instance on Ubuntu.

<!-- more -->

Note: This script is purely intended for use in short-lived demo systems. The passwords are obvious (`password` !?) and there is no hardening applied to any of this system. **DO NOT USE THIS SCRIPT IN PRODUCTION**. 

# Create Shell Script
Spin up an Ubuntu instance then create a new shell script and give it executable permissions:

```
touch osTicket.sh
chmod +x osTicket.sh
```

# Script Content
Paste this into the script:

```
#!/usr/bin/env bash

sudo apt update -y
sudo apt install unzip apache2 php7.2 php7.2-mysql mysql-server -y
sudo a2enmod rewrite
sudo rm /var/www/html/index.html
mkdir osticket && cd osticket
wget https://github.com/osTicket/osTicket/releases/download/v1.14.1/osTicket-v1.14.1.zip
unzip osTicket-v1.14.1.zip
sudo mv upload/* /var/www/html
sudo mv /var/www/html/include/ost-sampleconfig.php /var/www/html/include/ost-config.php
sudo chmod 0666 /var/www/html/include/ost-config.php
sudo mysql -u root -e "CREATE DATABASE osticket;"
sudo mysql -u root -e "CREATE USER 'osticket'@'localhost' IDENTIFIED BY 'password';"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON * . * TO 'osticket'@'localhost';"
sudo chown ubuntu:ubuntu /etc/apache2/sites-available/000-default.conf
cat <<EOF >> /etc/apache2/sites-available/000-default.conf
<Directory /var/www/>
AllowOverride All
</Directory>
EOF
sudo service apache2 restart
```

# Install via UI

Open a browser and navigate to `http://IPADDRESS/setup` and follow the wizard.

The script has created a database already (I advise adjusting these details for security):

* Database Name: `osticket`
* Database User: `osticket`
* Database Password: `password`

Note: You may get an HTTP `500` error during the install. That's fine. Just refresh the page and it'll work.


# Cleanup after Install

After the installation, you'll need to delete the `setup` directory and reset some file permissions. Just run this:

```
sudo rm -rf /var/www/html/setup
sudo chmod 0644 /var/www/html/include/ost-config.php
```

# Conclusion
At this point, you should have a fully working osTicket installation. Enjoy!

