---
layout: post
title: Automatic Tag Rules - Autonomous Monitoring
header_image: /images/headerimages/automatic-tag-rules-header.png
categories: [tagging, dynatrace, autonomous monitoring, acm, automation]
---

Part four of my autonomous cloud management (ACM) tutorial series. In this article we’ll look at an API driven way to apply tags to all of your entities (hosts, processes, process groups / clusters and services).

This tutorial series builds from previous tutorials. I recommend you complete parts 1 through 3 first:

- [Part one (Host Group Naming)](assured-host-groups-autonomous-monitoring)
- [Part two (Host Metadata)](automated-host-metadata-autonomous-monitoring)
- [Part three (Service & Process Group Naming)](service-process-group-naming-autonomous-monitoring)

## Tutorial Aim

![]({{ site.baseurl }}/images/postimages/automatic-tag-rules-1.png)

This tutorial will leverage the custom metadata we’ve already applied, we’ll create automatic (dynamic) tag rules so that we can use these values as filters.

## Recap

Recall that in the previous tutorials we added the following metadata tags to each host (with unique values for each host):

{% raw %}
```json
"metadata": {
       "Location": "DE",
       "ConsumingRegion": "Global",
       "Owner": "Alice",
       "ChargeCode": "Central"
   }
```
{% endraw %}

![]({{ site.baseurl }}/images/postimages/automatic-tag-rules-2.png)

It would be extremely powerful to have the ability to use these values as filters:

- Show me all hosts with a `ChargeCode` of `Central`.
- Show me all hosts and services for which `Alice` is responsible.
- Show me all hosts in `France`.

## How?

### API Token

The first thing we need is an API Token. Go to Settings > Integration > Dynatrace API and create your token.

Make sure it has at least `Write configuration` permissions.

![]({{ site.baseurl }}/images/postimages/automatic-tag-rules-3.png)

## Call API Via Ansible

We’ll use Ansible to call the Dynatrace API. This will create the rule definitions. We’ll create a separate task for each rule.

First, add two variables to the `vars` section near the top of your playlist: `tenant_url` and `api_write_token`. Adjust the values as appropriate for your environment.

{% raw %}
```yaml
vars:
  tenant_url: abc123456.live.dynatrace.com
  api_write_token: xYz123ABCdef678
```
{% endraw %}

Now create one API call. I’ll define it, explain it below, then copy & paste 3 more times, modifying as we go:

{% raw %}
```json
- name: Create ChargeCode Auto Tag Rule
  run_once: true
  uri:
    method: PUT
    status_code: 201, 204
    body_format: json
    url: https://{{ tenant_url }}/api/config/v1/autoTags/12345678-1234-1234-1234-123456789012?Api-Token={{api_write_token }}
    body: |
      {
        "name": "ChargeCode",
        "rules": [
        {
          "type": "PROCESS_GROUP",
          "enabled": true,
          "valueFormat": "{Host:Environment:ChargeCode}",
          "propagationTypes": [
            "PROCESS_GROUP_TO_HOST",
            "PROCESS_GROUP_TO_SERVICE"
          ],
          "conditions": [
              {
              "key": {
                "attribute": "HOST_CUSTOM_METADATA",
                "dynamicKey": {
                  "source": "ENVIRONMENT",
                  "key": "ChargeCode"
                },
                "type": "HOST_CUSTOM_METADATA_KEY"
              },
              "comparisonInfo": {
                "type": "STRING",
                "operator": "EXISTS",
                "value": null,
                "negate": false,
                "caseSensitive": null
              }
            }
            ]
        }
        ]
      }
```

## Task Explanation
We could improve the Ansible code here in numerous ways. If you’re comfortable enough with Ansible, please feel free to do so. I’ve deliberately left the example verbose for clarity.

The task is called `Create ChargeCode Auto Tag Rule`. Remember that we have two hosts in our inventory. We only need to execute this API call (aka run this task) once. Hence the run_once command.

We are executing a `PUT` call to the API and the URL format is:

{% raw %}
```
https://TENANT-URL/api/config/v1/autoTags/TAG-UUID?Api-token=API-WRITE-TOKEN
```
{% endraw %}

Note that the `UUID` is something you define and it must be in the standard `8-4-4-4-12` format. Being a unique ID, it must also be, err, unique, for each tag. Clever huh?

Within the `PUT` call, we will be passing in body content which defines our tag rule. The format of the body is JSON. Hence `body_format: json`.

The Dynatrace API returns one of two HTTP response codes on a successful call. A `201` response means everything was OK & your tag rule was successfully created. A `204` code means that your tag was updated successfully. This means you can re-execute your Ansible playbook multiple times with no ill effects. The `status_code` rule tells Ansible to consider `201` and `204` as successful calls.

`body` is obviously the `PUT` body content. Every tag is a `Key=Value` pair. The Key is represented by the name parameter. This tag rule will be enabled and the ruleset will match against to process groups.

Any tags applied to the process group will be propagated down to the hosts that they run on. The tags will also be propagated up to the services offered by those processes / process groups. This is denoted within the `propagationTypes` parameter.

The `conditions` and `comparisonInfo` work together to denote that this tag rule will match whenever the String value of `ChargeCode` exists. If found, the value of this tag will be pulled from the value of the host metadata (see the `valueFormat` parameter).

All together, this means that whenever the `ChargeCode` host metadata tag is found, Dynatrace will create a tag with the `Key=ChargeCode` and a dynamic value.

CREATE OTHER TAG API CALLS

Copy and paste the above Ansible tasks 3 more times. Change the UUID value for each and change ChargeCode to match the other Keys (ConsumingRegion, Location and Owner).

Your final playbook (including previous tutorials) should look something like this:

{% raw %}
```
---
- name: ACM Tutorial Playbook
  hosts: apache

  vars:
    hostList: "{{ lookup('file', 'hostList.json') }}"
    oneagent_installer_script_url: "https://{{ tenant_url}}/api/v1/deployment/installer/agent/unix/default/latest?Api-Token=***&arch=x86&flavor=default"
    defaultHostGroup: "DefaultGroup"
    tenant_url: "***.live.dynatrace.com"
    api_write_token: "***"

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
    shell: "sh /tmp/dynatrace-oneagent.sh APP_LOG_CONTENT_ACCESS=1 HOST_GROUP={{ hostvars[inventory_hostname].hostGroup | default(defaultHostGroup)  }}"
    become: yes
    when: agent_installed.stat.exists == False

  - name: Get Current Host Group
    shell: "/opt/dynatrace/oneagent/agent/tools/lib64/oneagentutil --get-host-group"
    become: yes
    when: agent_installed.stat.exists == True
    register: currentHostGroup

  - name: Update HOST_GROUP
    shell: "/opt/dynatrace/oneagent/agent/tools/lib64/oneagentutil --set-host-group {{ hostvars[inventory_hostname].hostGroup | default(defaultHostGroup) }} && sudo service oneagent restart"
    become: yes
    when: agent_installed.stat.exists == True and currentHostGroup.stdout != (hostvars[inventory_hostname].hostGroup | default(defaultHostGroup))

  - name: "Set Facts"
    set_fact:
     "metadata" : "{{ item.metadata }}"
    loop: "{{ hostList }}"
    when: item.hostname == inventory_hostname

  - name: "Remove File if it Exists"
    become: yes
    file:
      path: /var/lib/dynatrace/oneagent/agent/config/hostcustomproperties.conf
      state: absent

  - name: "Write KVs to File"
    become: yes
    lineinfile:
      path: /var/lib/dynatrace/oneagent/agent/config/hostcustomproperties.conf
      line: "{{ item.key }}={{ item.value }}"
      create: yes
    with_dict: "{{ hostvars[inventory_hostname]['metadata'] }}"

  - name: Install HTTPD (Apache)
    become: yes
    package:
      name: httpd
      state: present

  - name: Start HTTPD (Apache)
    become: yes
    service:
      name: httpd
      state: started

  - name: Create ChargeCode Auto Tag Rule
    run_once: true
    uri:
      method: PUT
      status_code: 201, 204
      body_format: json
      url: https://{{ tenant_url }}/api/config/v1/autoTags/12345678-1234-1234-1234-123456789012?Api-Token={{ api_write_token }}
      body: |
        {
          "name": "ChargeCode",
          "rules": [
          {
            "type": "PROCESS_GROUP",
            "enabled": true,
            "valueFormat": "{Host:Environment:ChargeCode}",
            "propagationTypes": [
            "PROCESS_GROUP_TO_HOST",
            "PROCESS_GROUP_TO_SERVICE"
          ],
          "conditions": [
              {
              "key": {
                "attribute": "HOST_CUSTOM_METADATA",
                "dynamicKey": {
                  "source": "ENVIRONMENT",
                  "key": "ChargeCode"
                },
                "type": "HOST_CUSTOM_METADATA_KEY"
              },
              "comparisonInfo": {
                "type": "STRING",
                "operator": "EXISTS",
                "value": null,
                "negate": false,
                "caseSensitive": null
              }
            }
            ]
          }
        ]
        }

  - name: Create ConsumingRegion Auto Tag Rule
    run_once: true
    uri:
      method: PUT
      status_code: 201, 204
      body_format: json
      url: https://{{ tenant_url }}/api/config/v1/autoTags/23456789-2345-2345-2345-234567890123?Api-Token={{ api_write_token }}
      body: |
        {
          "name": "ConsumingRegion",
          "rules": [
          {
            "type": "PROCESS_GROUP",
            "enabled": true,
            "valueFormat": "{Host:Environment:ConsumingRegion}",
            "propagationTypes": [
            "PROCESS_GROUP_TO_HOST",
            "PROCESS_GROUP_TO_SERVICE"
          ],
          "conditions": [
              {
              "key": {
                "attribute": "HOST_CUSTOM_METADATA",
                "dynamicKey": {
                  "source": "ENVIRONMENT",
                  "key": "ConsumingRegion"
                },
                "type": "HOST_CUSTOM_METADATA_KEY"
              },
              "comparisonInfo": {
                "type": "STRING",
                "operator": "EXISTS",
                "value": null,
                "negate": false,
                "caseSensitive": null
              }
            }
            ]
          }
        ]
        }

  - name: Create Location Auto Tag Rule
    run_once: true
    uri:
      method: PUT
      status_code: 201, 204
      body_format: json
      url: https://{{ tenant_url }}/api/config/v1/autoTags/34567890-3456-3456-3456-345678901234?Api-Token={{ api_write_token }}
      body: |
        {
          "name": "Location",
          "rules": [
          {
            "type": "PROCESS_GROUP",
            "enabled": true,
            "valueFormat": "{Host:Environment:Location}",
            "propagationTypes": [
            "PROCESS_GROUP_TO_HOST",
            "PROCESS_GROUP_TO_SERVICE"
          ],
          "conditions": [
              {
              "key": {
                "attribute": "HOST_CUSTOM_METADATA",
                "dynamicKey": {
                  "source": "ENVIRONMENT",
                  "key": "Location"
                },
                "type": "HOST_CUSTOM_METADATA_KEY"
              },
              "comparisonInfo": {
                "type": "STRING",
                "operator": "EXISTS",
                "value": null,
                "negate": false,
                "caseSensitive": null
              }
            }
            ]
          }
        ]
        }
    
  - name: Create Owner Auto Tag Rule
    run_once: true
    uri:
      method: PUT
      status_code: 201, 204
      body_format: json
      url: https://{{ tenant_url }}/api/config/v1/autoTags/45678901-4567-4567-4567-456789012345?Api-Token={{ api_write_token }}
      body: |
        {
          "name": "Owner",
          "rules": [
          {
            "type": "PROCESS_GROUP",
            "enabled": true,
            "valueFormat": "{Host:Environment:Owner}",
            "propagationTypes": [
            "PROCESS_GROUP_TO_HOST",
            "PROCESS_GROUP_TO_SERVICE"
          ],
          "conditions": [
              {
              "key": {
                "attribute": "HOST_CUSTOM_METADATA",
                "dynamicKey": {
                  "source": "ENVIRONMENT",
                  "key": "Owner"
                },
                "type": "HOST_CUSTOM_METADATA_KEY"
              },
              "comparisonInfo": {
                "type": "STRING",
                "operator": "EXISTS",
                "value": null,
                "negate": false,
                "caseSensitive": null
              }
            }
            ]
          }
        ]
        }
```
{% endraw %}

We now have hosts, processes, process groups and services all automatically tagged based on the content of the host metadata. The host metadata is, in itself, dynamic because it’s based on a JSON file.


![]({{ site.baseurl }}/images/postimages/automatic-tag-rules-4.png)

As always, the latest version of the host list [JSON](https://github.com/agardnerIT/OddFiles/blob/master/consistentHostListMetadata.json) and playbook is available on [Github](https://github.com/agardnerIT/OddFiles/blob/master/acmTutorial.playbook.yml).
