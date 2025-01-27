---

title: Assured Host Groups - Autonomous Monitoring
header_image: /images/headerimages/assured-host-groups-header.png
categories:
- host groups
- dynatrace
- autonomous monitoring
- acm
- automation
date:
  created: 2019-03-19
---

This is the first in a series of tutorials aimed at ensuring your Dynatrace deployment is (autonomous) cloud-ready. This tutorial will demonstrate how to set & keep your host groups in sync.

<!-- more -->

Dynatrace is already extremely automated. The out-of-the-box behaviour is almost install-and-forget. However, I consider it a best practice to configure host groups. They’ve saved me many times, especially as deployments grow larger and larger.

Host Groups are simple to set, just append the `--set-host-group=something` parameter to the install string.

{% raw %}
```
sudo /bin/sh/oneagent.sh ...other params... --set-host-group=something
```
{% endraw %}

That said, how do you keep thousands of hosts in sync during massive deployments? Moreover, how do you do this automatically?

## The Master List

First, you need some sort of agreed master list. This is the list which will always be in sync with your latest values. As cloud-natives, you’ll most likely be storing this in a Git / SVN repository. Obviously, you could also build this logic into a dynamic inventory system, but we’ll keep things simple for this tutorial – save the playbook and JSON in the same folder.

My JSON looks like this:

{% raw %}
```json
[{
  "hostname": "host1",
  "hostGroup": "something"
}, {
   "hostname": "IP-ADDRESS",
   "hostGroup": "FirstGroup"
}, {
   "hostname": "IP-ADDRESS",
   "hostGroup": "SecondGroup"
}]
```
{% endraw %}

## The Automation Script

It’s no secret that I love Ansible, so that’s what I’ll use here. However, there’s no reason why the concepts can’t be adapted for any automation / configuration management system.

Once configured, I’d have my Ansible playbook running on a schedule (or if your master list is on Git, you could run on each code commit).

This script is going to:

- Check whether the OneAgent is installed.
- If it isn’t installed, lookup the host group value from the JSON and install the agent. If the JSON does not contain a host group value, fallback to a default.
- If it is installed, check the current host group value against the JSON definition. If the JSON is different, reconfigure the agent and restart the OneAgent.
- Remember to replace `***` with your own tenant ID and API Key.

{% raw %}
```yaml
---
- name: Ensure Consistent Host Groups
  hosts: all

  vars:
    hostList: "{{ lookup('file', 'hostList.json') }}"
    oneagent_installer_script_url: "https://***.live.dynatrace.com/api/v1/deployment/installer/agent/unix/default/latest?Api-Token=***&arch=x86&flavor=default"
    defaultHostGroup: "DefaultGroup"

  tasks:
  - name: Check if Dynatrace OneAgent is already installed
    stat:
      path: /opt/dynatrace/oneagent/agent/lib64/liboneagentos.so
    register: agent_installed

  - name: Set Host Group Facts
    set_fact:
      hostGroup: "{{ item.hostGroup }}"
    loop: "{{ hostList }}"
    when: item.hostname == inventory_hostname

  - name: Download OneAgent
    get_url:
      url: "{{ oneagent_installer_script_url }}"
      dest: "/tmp/dynatrace-oneagent.sh"
    when: agent_installed.stat.exists == False

  - name: Install Agent
    shell: "sh /tmp/dynatrace-oneagent.sh --set-app-log-content-access=true --set-infra-only=false --set-host-group={{ hostvars[inventory_hostname].hostGroup | default(defaultHostGroup)  }}"
    become: yes
    when: agent_installed.stat.exists == False

  - name: Get Current Host Group
    shell: "/opt/dynatrace/oneagent/agent/tools/lib64/oneagentutil --get-host-group"
    become: yes
    when: agent_installed.stat.exists == True
    register: currentHostGroup

  - name: Update Host Group
    shell: "/opt/dynatrace/oneagent/agent/tools/lib64/oneagentutil --set-host-group={{ hostvars[inventory_hostname].hostGroup | default(defaultHostGroup) }} --restart-service"
    become: yes
    when: agent_installed.stat.exists == True and currentHostGroup.stdout != (hostvars[inventory_hostname].hostGroup | default(defaultHostGroup))
```
{% endraw %}

I hope this tutorial has given you some helpful hints and insight into how you can further automate your Dynatrace deployment. As always, questions, comments, suggestions or corrections are most welcome. Just [contact me](../contact.md).

The latest [playbook](https://github.com/agardnerIT/OddFiles/blob/master/consistentHostGroups.playbook.yml) and [JSON file](https://github.com/agardnerIT/OddFiles/blob/master/consistentHostGroup.json) for this tutorial can always be found on Github.