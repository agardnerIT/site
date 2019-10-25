---
layout: post
title: Automatic Application Definitions - Autonomous Monitoring
header_image: /images/headerimages/app-definitions-header.png
categories: [applications, dynatrace, autonomous monitoring, acm]
---

Part five of my autonomous cloud management (ACM) tutorial series. In this post we'll use the Dynatrace API to automatically define front-end applications, which are based on URL patterns.

This tutorial series builds from previous tutorials. I recommend you complete parts 1 through 4 first:

- [Part one (Host Group Naming)](/assured-host-groups-autonomous-monitoring)
- [Part two (Host Metadata)](/assured-host-metadata-autonomous-monitoring)
- [Part three (Service & Process Group Naming)](/service-process-group-naming-autonomous-monitoring)
- [Part four (Automatic Tag Rules)](/automatic-tag-rules-autonomous-monitoring)

## Recap

Following previous tutorials has given us 2 EC2 instances, both with a single Apache HTTP server running. One is the `production` server and the other is the `staging` server. We have split the process groups and services accordingly so that the Davis AI engine will alert separately for production and staging. We've also applied various tags due to the metadata so that we can create flexible filters.

## Scenario

Imagine that we have two different front-end URLs for our `production` and `staging` servers: `mysite.com` and `staging.mysite.com` respectively.

We need to tell Dynatrace to group the traffic into different “buckets” or applications, based on these URL patterns. We need to do this automatically as part of our pipeline so that we can easily onboard new environments and commit all the configuration as code.

## Concepts

Dynatrace provides the ability to create Applications. An application is nothing more than a logical bucket, based on a domain or URL pattern. An application can have one or more rules associated with it. All user sessions and user action data (what the user did on your website) will be matched to a specific application.

Applications can also exist for mobile (native applications) and a special type of application, called an agentless application. Mobile and agentless applications are out of scope of this post.

## My Web Application - A Note

You may notice an application in Dynatrace called "My web application". Think of this as the default "catch-all" bucket. If traffic arrives that does not match any other rules, it will fall into this bucket.

In a correctly configured system, there should be no traffic in "My web application".

## Application Definition as JSON

Creating a Dynatrace application is a three step process:

- Create the application & configure settings such as the percentage of user traffic to capture or telling Dynatrace which Javascript frameworks your site uses.
- Create the URL mapping rule. This provides the mapping between the URL (or domain) and the application.
- Apply tags to the applications.

Create three new JSON files. The first to hold details of the application and configuration details.
The second to hold the URL mapping rules for the applications defined in the first JSON.
The third to hold the tags you wish to assign to each application. Both the application and rules have unique IDs. The rule maps to the application by using the application ID.

Note: The application ID format is `APPLICATION-{16 digit uppercase HEX value}`.
The application rules ID format is any valid `8-4-4-4-12` GUID.

### appList.json

{% raw %}
```json
[{
    "id": "APPLICATION-0000000000000001",
    "name": "Staging App"
},
{
    "id": "APPLICATION-0000000000000002",
    "name": "Production App"
}]
```
{% endraw %}

### appRules.json

{% raw %}
```json
[{
    "id": "00000000-0000-0000-0000-000000000100",
    "appId": "APPLICATION-0000000000000001",
    "pattern": "staging.mysite.com",
    "matchType": "CONTAINS",
    "matchTarget": "URL"
},
{
    "id": "00000000-0000-0000-0000-000000000200",
    "appId": "APPLICATION-0000000000000002",
    "pattern": "mysite.com",
    "matchType": "CONTAINS",
    "matchTarget": "URL"
}]
```
{% endraw %}

If you're following the previous parts of the tutorial, we obviously don't have domain names setup for our instances. So if you want to see traffic assigned to these applications, use the public IPs of your EC2 instances rather than the domain names.

For example, replace `staging.mysite.com` with the public IP of your `staging` instance and replace `mysite.com` with the public IP of your `production` instance.

### appTags.json

{% raw %}
```json
[{
    "appId": "APPLICATION-0000000000000001",
    "tags": [ "mysite-staging" ]
},
{
    "appId": "APPLICATION-0000000000000002",
    "tags": [ "mysite-production" ]
}]
```
{% endraw %}

## Additional Token Permissions

Recall from previous steps in this series that your `api_write_token` had `write configuration` permissions.

To follow this tutorial, we need to give it one more permission: `Access problem and event feed, metrics, and topology.`

Your `api_write_token` should have two permissions now.

![](/images/postimages/app-definitions-1.png)

## Leverage Dynatrace APIs

Now we need to call the Dynatrace APIs to create our application. As mentioned above, this is a two step process.

First, let's create our application defintion using the `/config/v1/applications/web` endpoint with a JSON payload:

{% raw %}
```
PUT https://TENANT-URL/api/config/v1/applications/web/APPID?Api-Token=API-WRITE-TOKEN"
 
Body Content:
{
  "name": "APPLICATION NAME",
  "realUserMonitoringEnabled": true,
  "costControlUserSessionPercentage": 100,
  "loadActionKeyPerformanceMetric": "VISUALLY_COMPLETE",
  "xhrActionKeyPerformanceMetric": "ACTION_DURATION",
  "loadActionApdexSettings": {
    "toleratedThreshold": 3000,
    "frustratingThreshold": 12000,
    "toleratedFallbackThreshold": 3000,
    "frustratingFallbackThreshold": 12000,
    "considerJavaScriptErrors": true
  },
  "xhrActionApdexSettings": {
    "toleratedThreshold": 2500,
    "frustratingThreshold": 10000,
    "toleratedFallbackThreshold": 3000,
    "frustratingFallbackThreshold": 12000,
    "considerJavaScriptErrors": false
  },
  "customActionApdexSettings": {
    "toleratedThreshold": 3000,
    "frustratingThreshold": 12000,
    "toleratedFallbackThreshold": 3000,
    "frustratingFallbackThreshold": 12000,
    "considerJavaScriptErrors": true
  },
  "waterfallSettings": {
    "uncompressedResourcesThreshold": 860,
    "resourcesThreshold": 100000,
    "resourceBrowserCachingThreshold": 50,
    "slowFirstPartyResourcesThreshold": 200000,
    "slowThirdPartyResourcesThreshold": 200000,
    "slowCdnResourcesThreshold": 200000,
    "speedIndexVisuallyCompleteRatioThreshold": 50
  },
  "monitoringSettings": {
    "fetchRequests": false,
    "xmlHttpRequest": true,
    "javaScriptFrameworkSupport": {
      "angular": true,
      "dojo": false,
      "extJS": false,
      "icefaces": false,
      "jQuery": true,
      "mooTools": false,
      "prototype": true,
      "activeXObject": false
    },
    "contentCapture": {
      "resourceTimingSettings": {
        "w3cResourceTimings": true,
        "nonW3cResourceTimings": false,
        "nonW3cResourceTimingsInstrumentationDelay": 50,
        "resourceTimingCaptureType": "CAPTURE_FULL_DETAILS",
        "resourceTimingsDomainLimit": 10
      },
      "javaScriptErrors": true,
      "timeoutSettings": {
        "timedActionSupport": false,
        "temporaryActionLimit": 0,
        "temporaryActionTotalTimeout": 100
      },
      "visuallyCompleteAndSpeedIndex": true
    },
    "excludeXhrRegex": "",
    "injectionMode": "JAVASCRIPT_TAG",
    "libraryFileLocation": "",
    "monitoringDataPath": "",
    "customConfigurationProperties": "",
    "serverRequestPathId": "",
    "secureCookieAttribute": false,
    "cookiePlacementDomain": "",
    "cacheControlHeaderOptimizations": true,
    "advancedJavaScriptTagSettings": {
      "syncBeaconFirefox": false,
      "syncBeaconInternetExplorer": false,
      "instrumentUnsupportedAjaxFrameworks": false,
      "specialCharactersToEscape": "",
      "maxActionNameLength": 100,
      "maxErrorsToCapture": 10,
      "additionalEventHandlers": {
        "userMouseupEventForClicks": false,
        "clickEventHandler": false,
        "mouseupEventHandler": false,
        "blurEventHandler": false,
        "changeEventHandler": false,
        "toStringMethod": false,
        "maxDomNodesToInstrument": 5000
        },
      "eventWrapperSettings": {
        "click": false,
        "mouseUp": false,
        "change": false,
        "blur": false,
        "touchStart": false,
        "touchEnd": false
      },
      "globalEventCaptureSettings": {
        "mouseUp": true,
        "mouseDown": true,
        "click": true,
        "doubleClick": true,
        "keyUp": true,
        "keyDown": true,
        "scroll": true,
        "additionalEventCapturedAsUserInput": ""
      }
    }
  },
  "userActionNamingSettings": {
    "placeholders": [],
    "loadActionNamingRules": [],
    "xhrActionNamingRules": [],
    "ignoreCase": true
  }
}
```
{% endraw %}

Now use the `/config/v1/applicationDetectionRules` endpoint to create the mapping rule:

{% raw %}
```
PUT https://TENANT-URL/api/config/v1/applicationDetectionRules/RULEID?Api-Token=API-WRITE-TOKEN

Body Content:
{
  "applicationIdentifier": "APPLICATION-***********",
  "filterConfig": {
    "pattern": "myapp.example.com",
    "applicationMatchType": "BEGINS_WITH|CONTAINS|ENDS_WITH|EQUALS|MATCHES",
    "applicationMatchTarget": "DOMAIN|URL"
  }
}
```
{% endraw %}

## Tagging Applications

Finally, we'll tag our applications via the API, using the values held in `appTags.json`.

Use the `/api/v1/entity/applications/` endpoint. The `{APP-ID}` corresponds to our `APPLICATION-*` value and the tags array should be populate from the `appTags.json` file.

{% raw %}
```
POST https://TENANT-URL/api/v1/entity/applications/{APP-ID}

Body:
{
  "tags": [ // Tags from appTags.json ]
}
```
{% endraw %}

## Playbook

Let's add the above logic into our existing Ansible playbook (from the previous tutorial steps). Ensure all 4 files (`appList.json`, `appRules.json`, `appTags.json` and `yourPlaybook.yaml`) are all in the same folder.

Add three new variables to the vars section near the top of the playlist:

{% raw %}
```yaml
    app_list: "{{ lookup('file', 'appList.json') }}"
    app_rules: "{{ lookup('file', 'appRules.json') }}"
    app_tags: "{{ lookup('file', 'appTags.json') }}"
```
{% endraw %}

Now add the following tasks to the end of your playbook:

{% raw %}
```yaml
- name: Create Applications
    run_once: true
    loop: "{{ app_list }}"
    uri:
      url: "https://{{ tenant_url }}/api/config/v1/applications/web/{{ item.id }}?Api-Token={{ api_write_token }}"
      method: PUT
      status_code: 201, 204
      body_format: json
      body: |
        {
          "name": "{{ item.name }}",
          "realUserMonitoringEnabled": true,
          "costControlUserSessionPercentage": 100,
          "loadActionKeyPerformanceMetric": "VISUALLY_COMPLETE",
          "xhrActionKeyPerformanceMetric": "ACTION_DURATION",
          "loadActionApdexSettings": {
            "toleratedThreshold": 3000,
            "frustratingThreshold": 12000,
            "toleratedFallbackThreshold": 3000,
            "frustratingFallbackThreshold": 12000,
            "considerJavaScriptErrors": true
          },
          "xhrActionApdexSettings": {
            "toleratedThreshold": 2500,
            "frustratingThreshold": 10000,
            "toleratedFallbackThreshold": 3000,
            "frustratingFallbackThreshold": 12000,
            "considerJavaScriptErrors": false
          },
          "customActionApdexSettings": {
            "toleratedThreshold": 3000,
            "frustratingThreshold": 12000,
            "toleratedFallbackThreshold": 3000,
            "frustratingFallbackThreshold": 12000,
            "considerJavaScriptErrors": true
          },
          "waterfallSettings": {
            "uncompressedResourcesThreshold": 860,
            "resourcesThreshold": 100000,
            "resourceBrowserCachingThreshold": 50,
            "slowFirstPartyResourcesThreshold": 200000,
            "slowThirdPartyResourcesThreshold": 200000,
            "slowCdnResourcesThreshold": 200000,
            "speedIndexVisuallyCompleteRatioThreshold": 50
          },
          "monitoringSettings": {
            "fetchRequests": false,
            "xmlHttpRequest": true,
            "javaScriptFrameworkSupport": {
              "angular": true,
              "dojo": false,
              "extJS": false,
              "icefaces": false,
              "jQuery": true,
              "mooTools": false,
              "prototype": true,
              "activeXObject": false
            },
            "contentCapture": {
              "resourceTimingSettings": {
                "w3cResourceTimings": true,
                "nonW3cResourceTimings": false,
                "nonW3cResourceTimingsInstrumentationDelay": 50,
                "resourceTimingCaptureType": "CAPTURE_FULL_DETAILS",
                "resourceTimingsDomainLimit": 10
              },
                "javaScriptErrors": true,
              "timeoutSettings": {
                "timedActionSupport": false,
                "temporaryActionLimit": 0,
                "temporaryActionTotalTimeout": 100
              },
              "visuallyCompleteAndSpeedIndex": true
            },
            "excludeXhrRegex": "",
            "injectionMode": "JAVASCRIPT_TAG",
            "libraryFileLocation": "",
            "monitoringDataPath": "",
            "customConfigurationProperties": "",
            "serverRequestPathId": "",
                "secureCookieAttribute": false,
            "cookiePlacementDomain": "",
            "cacheControlHeaderOptimizations": true,
            "advancedJavaScriptTagSettings": {
              "syncBeaconFirefox": false,
              "syncBeaconInternetExplorer": false,
              "instrumentUnsupportedAjaxFrameworks": false,
              "specialCharactersToEscape": "",
              "maxActionNameLength": 100,
              "maxErrorsToCapture": 10,
              "additionalEventHandlers": {
                "userMouseupEventForClicks": false,
                "clickEventHandler": false,
                "mouseupEventHandler": false,
                "blurEventHandler": false,
                "changeEventHandler": false,
                "toStringMethod": false,
                "maxDomNodesToInstrument": 5000
              },
              "eventWrapperSettings": {
                "click": false,
                "mouseUp": false,
                "change": false,
                "blur": false,
                "touchStart": false,
                "touchEnd": false
                },
              "globalEventCaptureSettings": {
                "mouseUp": true,
                "mouseDown": true,
                "click": true,
                "doubleClick": true,
                "keyUp": true,
                "keyDown": true,
                "scroll": true,
                "additionalEventCapturedAsUserInput": ""
                }
              }
            },
            "userActionNamingSettings": {
            "placeholders": [],
            "loadActionNamingRules": [],
                "xhrActionNamingRules": [],
              "ignoreCase": true
          }
        }

  - name: Create Application Rules
    run_once: true
    loop: "{{ app_rules }}"
    uri:
      url: "https://{{ tenant_url }}/api/config/v1/applicationDetectionRules/{{ item.id }}?Api-Token={{ api_write_token }}"
      method: PUT
      status_code: 201, 204
      body_format: json
      body: |
        {
          "applicationIdentifier": "{{ item.appId }}",
          "filterConfig": {
          "pattern": "{{ item.pattern }}",
          "applicationMatchType": "{{ item.matchType }}",
          "applicationMatchTarget": "{{ item.matchTarget }}"
          }
        }

  - name: Create Application Tags
    run_once: true
    loop: "{{ app_tags }}"
    uri:
      url: "https://{{ tenant_url }}/api/v1/entity/applications/{{ item.appId }}?Api-Token={{ api_write_token }}"
      method: POST
      status_code: 201, 204
      body_format: json
      body: |
        {
          "tags": {{ item.tags }},
        }
```
{% endraw %}

Execute your playbook and view the results in Dynatrace.

Go to "Applications" and you should see two new applications: `Staging App` and `Production App`.

Drill into each applications to see the tags and URL rules.

## Result

![](/images/postimages/app-definitions-2.png)
