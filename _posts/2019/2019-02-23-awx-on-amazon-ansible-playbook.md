---
layout: post
title: AWX on Amazon Ansible Playbook
header_image: /images/headerimages/awx-header.jpg
categories: [aws, ansible, awx]
---

Today I spent a good few hours trying to get the [Geerling Guy AWX role](https://galaxy.ansible.com/geerlingguy/awx) to work. AWX is the open source, free version of Ansible Tower. Suffice to say, the combination of dependencies is sufficiently broken to be (currently) useless. Here’s the fix...

However, I have put together a handy playbook which **does** work for Amazon AMIs (specifically, I used the 2018.03.0 AMI).

Here’s the playbook (latest version will always be on [GitHub](https://github.com/agardnerIT/ansible-playbook-awx)):

{% raw %}
```yaml
---
- name: Install AWX
  hosts: awx
  become: yes

  vars:
    - tmpdir: "/tmp/ansible"

  tasks:

  - name: Update yum
    yum:
      name: '*'
      state: latest

  - name: Install Ansible
    pip:
      name: ansible
      state: latest

  - name: Install Repositories
    yum:
      name: "{{ item }}"
    loop:
      - git
      - docker

  - name: Start Docker
    service:
      name: docker
      state: started

  - name: Clone awx
    git:
      repo: 'https://github.com/ansible/awx.git'
      dest: "{{ tmpdir }}"
      clone: yes

  - name: Install Docker Compose
    pip:
      name: docker-compose
      state: latest

  - name: Install AWX
    command: /usr/local/bin/ansible-playbook -i {{ tmpdir }}/installer/inventory {{ tmpdir }}/installer/install.yml
```
{% endraw %}

AWX runs on port 80. The login is `admin` / `password`.

![](/images/postimages/awx-playbook-1.png)

If you have any questions, comments or suggestions. Please [contact me](contact) or raise a [GitHub issue](https://github.com/agardnerIT/ansible-playbook-awx/issues).