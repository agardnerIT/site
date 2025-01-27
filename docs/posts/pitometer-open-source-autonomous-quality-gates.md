---

title: Pitometer - Open Source Autonomous Quality Gates
header_image: /images/headerimages/pitometer-quality-gates-header.jpg
categories:
- automation
- devops
- keptn
- open source
- pitometer
date:
  created: 2019-06-07
---

!!! warning "Legacy Service"
    This tutorial refers to the legacy "Pitometer" service which has now been superceded by [KEPTN QUALITY GATES](https://keptn.sh).
    
    I recommend reading this [Keptn + Prometheus Tutorial](https://medium.com/keptn/implementing-sli-slo-based-continuous-delivery-quality-gates-using-prometheus-9e17ec18ca36) instead.

Imagine releasing software with zero upfront meetings. Imagine a release that was tested and promoted (or rejected) through your pipeline automatically. Imagine being able to mix and match the tools that provide those metrics. Imagine a world where you didn’t constantly argue over release acceptance / quality criteria. Imagine an open source tool that did all of that. Meet Pitometer...

<!-- more -->

Pitometer is an open source tool which allows you to specify your definitions of software quality in code, pull metrics from **anywhere**, then automatically grade your software into pass, warning or fail states.

Your pipeline can then leverage that decision to promote or reject the deployment.

Pitometer is a module within the [keptn project](https://keptn.sh/) (more on keptn in future blog posts). However Pitometer can also be used as a standalone tool in any environment, **not only cloud native environments**.

## Simple Example

- You have an upcoming code deployment.
- You know the figures you need to hit. The business have signed off on them.
- You’re using both Prometheus and Dynatrace to monitor various parts of the system.

## Criteria 1 - Throughput

- Measured by: Prometheus
- Success Criteria: 100 requests per second.

## Criteria 2 - Response time

- Measured by: Dynatrace
- Success Criteria: Average response time less than 3 seconds.

## Translation To Pitometer

Let’s translate the above into Pitometer code.

Crucially, this performance as code specification can be committed to any code repository, just like your source code.

{% raw%}
```json
{
  "indicators": [
  {
    "id": "prometheus_throughput",
    "source": "Prometheus",
    "query": "rate(http_requests_total)",
    "grading": {
      "type": "Threshold",
      "thresholds": {
        "lowerWarning": 110,
        "lowerSevere": 100
      },
      "metricScore": 50
    }
  },
  {
    "id": "dynatrace_response_time",
    "source": "Dynatrace",
    "query": {
      "timeseriesId": "com.dynatrace.builtin:service.responsetime",
      "aggregation": "avg"
    },
    "grading": {
        "type": "Threshold",
        "thresholds": {
          "upperSevere": 3000000,
          "upperWarning": 2500000
        },
        "metricScore": 50
      }
  }],
  "objectives": {
    "pass": 90,
    "warning": 75
  }
}
```
{% endraw %}

## Explanation

We have specified two indicators. The first sources its data from Prometheus by running the `rate(http_requests_total)` query. Pitometer will then grade the results based on the Threshold grader.

Since we’re using lower thresholds, the results will be evaluated as "are they below the threshold?".

For example, a throughput value of 112 would be a `pass`. A throughput value of 109 would be in a `warning` state. A throughput of 100 or less would mean this indicator is in a `fail` state.

For thresholds, an indicator that passes gets 100% of the `metricScore`.

- An indicator in a `warning state` = 50% of metricScore.
- An indicator in a `fail state` = metricScore value of zero.

The second indicator pulls the average response time data from Dynatrace then evaluates against its thresholds.

- A response time above 2.5 seconds is in `warning state`.
- A response time above 3 seconds is in a `severe state`.

Both indicators are weighted equally (due to each having a `metricScore` of 50).

You can adjust the importance of each indicator by assigning different total weights to each metric score.

## Outcomes (Objectives)

The final block of code objectives evaluates both indicator results against a threshold.

- If the total metric score is above 90, the deployment is in a pass state.
- Between 75 and 90 and the deployment is a warning state.
- Below 75 and the deployment is in a fail state.

## Final Thoughts

- If you’re using Kubernetes, I highly recommend you use [keptn](https://keptn.sh), rather than a standalone implementation of Pitometer.
- You get all the benefits of Pitometer plus the awesome power of keptn.
- Pitometer follows the “everything as code” philosophy.
- No more meetings or arguments about deployment health!
- Pitometer can assess metrics from any source that is accessible via an API.
- If you can get the metrics out, Pitometer can evaluate them.

## Stay Tuned

If you’d like to know more about keptn or Pitometer, [contact me](../contact.md) or [follow me on LinkedIn](https://www.linkedin.com/in/agardner1/).

I’ll be releasing a full working demonstration system of Pitometer soon.

Stay tuned...
