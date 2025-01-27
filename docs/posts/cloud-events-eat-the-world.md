---

title: Why CloudEvents will Eat The World
categories:
- cloudevents
header_image: https://cloudevents.io/img/logos/cloudevents-icon-color.png
date:
  created: 2022-05-23
---

YAML and JSON have won the war for data exchange formats, but we still haven't standardised on *what* we say to each other. [CloudEvents](https://cloudevents.io) solve that problem.

<!-- more -->

# What Is Said, Not How It Is Said

Sending messages between tools using JSON is almost standard practice by now. But that is only half the equation. Take these two JSON documents. Each document contains the same information, they **say** the same thing, but in entirely different ways.

Document 1:
```
{
  "generator": "vendor A",
  "issue": {
    "id": "1",
    "impacted": [{
      "system": "system 1",
      "application": "appA" 
    }],
    "alert_type": "email",
    "alert_destination": "john.smith@example.com"
    "alert_when": "now"
  }
}
```

Document 2:
```
{
  "issue_id": "1",
  "systems_involved": [{
    "name": "system 1"
  }],
  "apps_involved": [{
    "name": "appA"
  }],
  "notification": "E",
  "notify_endpoint": "john.smith@example.com",
  "notify_delay": 0,
  "tool": "vendor B"
}
```

We humans have no issue understanding that these are ultimately conveying the same information, but that is harder for a computer to ascertain.

If a system wants to **consume** these alerts, the system needs to understand the content and context of the **sender**. In essence, the receiving system needs to know how to **parse and translate** the input into a format usable for its purposes.

This problem does not scale well. If I'm writing an alert ingestion system (which can send emails in response to incoming alerts, for example) I need to understand every possible input JSON format and write "decoders" for each tool.

# The Core Problem
No one has yet sat down and decided: If you want to send an alert (to continue the above example):
- Here is *how* you say it
- Here are the fields you **must** include (eg. the minimal information to make this understandable as an alert for a consuming system)
- We don't want to be too draconian and opinionated so here is a space for any custom or vendor-specific fields.

## CloudEvents: A Solution

The [CloudEvents](https://cloudevents.io) specification tackles this exact problem. The specification defines the basic outline of a message:

- The fields that **MUST** be included
- The fields that **MAY** be included
- A "spare" area for anything truly vendor specific

Transforming the above event to a cloudevent gives:

```
{
  "specversion": "1.0",
  "id": "1",
  "source": "vendor A",
  "type": "com.vendora.alert.triggered",
  "data": {
    "issue": {
      "id": "1",
      "impacted": [{
        "system": "system 1",
        "application": "appA" 
      }],
      "alert_type": "email",
      "alert_destination": "john.smith@example.com"
      "alert_when": "now"
    }
  }
}
```

An alert consumer can now easily understand that this is an `alert.triggered` event and that the `source` was `vendor A`. `vendor A` has included their custom fields inside the `data` block but even without that data, the consumer still knows this is an alert.

> CloudEvents define a standard syntax for describing events as they flow around, through and across system boundaries.

# What Types of CloudEvent are available?

CloudEvents define the specification, but are deliberately not descriptive on what types of events are created - so you're free to create your standards.

Contributors and companies I've seen utilising CloudEvents:

- [Google](https://github.com/googleapis/google-cloudevents)
- [Jenkins](https://github.com/jenkinsci/cloudevents-plugin)
- [Keptn](https://github.com/keptn/spec)
- [Alibaba](https://github.com/alibaba)
- [Confluent](https://github.com/confluentinc/event-streaming-patterns/blob/main/docs/event/event-envelope.md)
- Huawei
- IBM
- Oracle
- PayPal
- SAP
- RedHat
- and many many more. You'll be in good company.

# Use CloudEvents?
Does your product use CloudEvents? Have I missed anything in the article?
Want your name linked above? Drop me a line and let me know.