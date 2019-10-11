---
layout: post
title: Tomcat 9 on AWS CentOS
header_image: /images/headerimages/tomcat-aws-header.png
categories: [aws, centos]
---

The Amazon Linux AMI 2018.03.0 image comes with Tomcat 7 and 8. Copy and paste this code into your SSH terminal to install Java 8 and Tomcat 9.

```bash
# Install Java 8
sudo yum install java-1.8.0-openjdk.x86_64 -y
# Set Java_HOME and JRE_HOME to java8
echo JAVA_HOME="/usr/lib/jvm/jre-1.8.0-openjdk.x86_64" | sudo tee -a /etc/profile
echo JRE_HOME="/usr/lib/jvm/jre-1.8.0-openjdk.x86_64" | sudo tee -a /etc/profile
# Refresh JAVA_HOME and JRE_HOME
source /etc/profile
wget https://www-eu.apache.org/dist/tomcat/tomcat-9/v9.0.19/bin/apache-tomcat-9.0.19.tar.gz
tar xvf apache-tomcat-9.0.19.tar.gz
~/apache-tomcat-9.0.19/bin/startup.sh
# Server running at http://SERVERIP:8080
# If not, check ~/apache-tomcat-9.0.12/logs/catalina.out
```