---
layout: post
title: Ansible 101 - Vault
header_image: /images/headerimages/ansible-vault-header.png
categories:
- ansible
- automation
- devops
- vault
date:
  created: 2018-08-18
---

Ansible Vault is an out-of-the-box encryption mechanism. Use it to store (encrypted) sensitive data for use within playbooks. This tutorial will get you up-and-running with Ansible Vault in under 10 minutes.

<!-- more -->

## Prerequisites

If you haven’t already got hands-on experience with Ansible, I highly suggest you follow my previous tutorials:

- [Ansible 101: Ansible Basics](ansible-101-basics.md)
- [Ansible 101: Ansible Playbooks](ansible-101-playbooks.md)

Needless to say, you’ll need Ansible installed on a `control` machine. All commands in this article are to be executed on the control machine.

Note: For this tutorial, we’ll be running the playbook against the `localhost` meaning all commands will be executed on and targeted at, the `control` machine. The files will be copied to directories on the control machine.

## Scenario

Imagine we want to write a configuration file to a remote host. This configuration file contains sensitive information that should be held not held in plain text. The variable name is `foo` and the value is `bar`.

Let’s also assume that our origin file (the file on the control node that we want to copy to the target) contains this text and is called `myIniFile.ini`:

```
# Variables
foo = bar;
```

We could write our playbook like this:

```yaml
---
- name: Create File
hosts: localhost
connection: local

tasks:

- name: Write File
  template:
    src: ~/myIniFile.ini
    dest: /tmp/myIniFile.ini
```

However, this would expose our sensitive data to the world. **Dangerous stuff!**

Go ahead and create that INI file (and insert the contents as above). Also create the playbook (as above).

Run the playbook: `ansible-playbook myPlaybookFile.playbook`

You should expect to see a copy of the `myIniFile.ini` in `/tmp`.

## Encrypting the Sensitive Values

Now, let’s solve the problem and use **Ansible Vault** to encrypt our sensitive data. One of the things I love about Ansible is the great documentation. Take a look at the [vault docs page](https://docs.ansible.com/ansible/2.6/user_guide/vault.html) and you’ll see this:

> If you have existing files that you wish to encrypt, use the ansible-vault encrypt command:<br />`ansible-vault encrypt file1 file2 ...`

So let's encrypt our INI file:

```
ansible encrypt myIniFile.ini
```

Enter a vault password and confirm. You should a confirmation message: `Encryption Successful`

To confirm, view the INI file with your favourite editor and you’ll see the encrypted content. This encrypted file is safe to placed into version control systems.

```
$ cat myIniFile.ini
$ANSIBLE_VAULT;1.1;AES256
6166445334280909902380515325321
0809902525523587890285308235808
...
```

## Viewing Unencrypted Vault Data

To view the unencrypted contents of the file, use the `ansible-vault view` command:

```
ansible-vault view myIniFile.ini
```

## Vault Password Files

As an alternative to the above, you can store your password (plain text) in a file, then pass this file at runtime as a parameter.

Let’s say your password is `password123` and is stored in `/tmp/passwordfile`

Encrypt your INI file as such:

```
ansible-vault encrypt ~/myIniFile.ini --vault-id=/tmp/passwordfile
```

Then to decrypt, just change `encrypt` to `view`:

```
ansible-vault view ~/myIniFile.ini --vault-id=/tmp/passwordfile
```

Note that you can specify multiple files (and vault IDs) at once. Imagine `test.txt` is encrypted with the password in `passwordfile` and `test2.txt` is encrypted with the password in `passwordfile2`.

This is a perfectly valid command:

```
ansible-vault view ~/test.txt ~/test2.txt --vault-id=~/passwordfile --vault-id=~/passwordfile2
```

## Re-Execute Playbook With Ansible Vault File

- Delete the old INI file in /tmp: `rm /tmp/myIniFile.ini`
- Re-run the playbook, adding the `--ask-vault-pass` option: `ansible-playbook makeFile.playbook --ask-vault-pass`
- Notice that the file is decrypted then copied into the `/tmp` directory