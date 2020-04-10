---
layout: post
title: Atlassian Bamboo Automated Install Script
header_image: /images/headerimages/bamboo.svg
categories: [atlassian, bamboo, cicd, automation, shell script]
---

[Atlassian Bamboo](https://www.atlassian.com/software/bamboo) is an extremely popular CICD platform. Here's an easy way to spin up an instance on Ubuntu.

I tested this on an AWS Ubuntu 18.04 `t3.small` instance. 

# Create Shell Script
Spin up an Ubuntu instance then create a new shell script and give it executable permissions:

```
touch bambooSetup.sh && chmod +x bambooSetup.sh
```

# Script Content
Paste this into the script:

```
#!/usr/bin/env bash

sudo apt-get update -y
sudo apt install openjdk-8-jdk-headless -y
sudo /usr/sbin/useradd --create-home --home-dir /usr/local/bamboo --shell /bin/bash bamboo
sudo mkdir /opt/bamboofiles
cd /opt
sudo wget https://product-downloads.atlassian.com/software/bamboo/downloads/atlassian-bamboo-7.0.2.tar.gz
sudo tar -xf /opt/atlassian-bamboo-7.0.2.tar.gz
sudo mv atlassian-bamboo-7.0.2 bamboo
# Set Bamboo Home which is NOT the same as the install directory
echo "bamboo.home=/opt/bamboofiles" | sudo tee --append /opt/bamboo/atlassian-bamboo/WEB-INF/classes/bamboo-init.properties > /dev/null
sudo chown -R bamboo: /opt/bamboo
sudo chown -R bamboo: /opt/bamboofiles
sudo -H -u bamboo /opt/bamboo/bin/start-bamboo.sh
echo ""
echo "================================================================"
echo "Bamboo Started!"
echo "Bamboo Available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8085"
echo "================================================================"
echo ""
```

Once complete, you'll see the Bamboo address printed to the console where `1.2.3.4` is your VM public IP address.

```
================================================================
Bamboo Started!
Bamboo Available at: http://1.2.3.4:8085"
================================================================
```

# Conclusion
At this point, you should have a fully working Atlassian Bamboo installation. Follow the browser instructions to generate a license key and activate Bamboo.

