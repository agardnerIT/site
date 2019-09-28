---
layout: post
title: Dynatrace Basics - Creating Measures
permalink: dynatrace-basics-creating-measures
categories: [measures, dynatrace, appmon]
---

This tutorial will how to setup long term trending of your applications and key transactions in Dynatrace AppMon. It will use a concept called **measures**.

**NOTE: THIS TUTORIAL REFERS TO THE LEGACY APPLICATION MONITORING PRODUCT FROM DYNATRACE NOT THE DYNATRACE PLATFORM.**

## What is a Measure?

Put simply, it’s a piece of your application that you wish to measure. Dynatrace will automatically create Purepaths for every transaction (Dynatrace does not sample data) but for long term trending, you’ll want to explicitly set up a measure on the transaction. Once done, the data will be stored forever in the Dynatrace database (performance warehouse).

> Measures are the way to track long term trends in metrics.

## The Business Requirement

Imagine that the business has given us 3 requirements:

1. Track the response time of the batch job.
2. Track the response time of the batch job when the batch type is Type B.
3. Track the response time of the batch job per execution type (ie. response time of Type A vs. Type B).

## Demo Code

Here’s the [demo JAR file](https://github.com/agardnerIT/DTBasicsCreatingMeasures/releases/download/1.0/DTBasicsCreatingMeasures.jar) we’ll be using in this tutorial (and here’s the [source code on Github](https://github.com/agardnerIT/DTBasicsCreatingMeasures) if you want it).

The JAR file randomly calculates a boolean and if it’s true, the batch is said to be “Type A”. If false, the batch is “Type B”. If the batch is “Type B”, the process pauses for an extra 3 seconds (the reason for this will become clear later).

```java
/* Randomly pick A or B
* Arbitrarily, if true it’s “Type A” if false it’s “Type B”
* Note: We use Strings to make it clearer to the reader.
* Dynatrace AppMon works perfectly well with booleans or numbers or anything else.
*/
String strBatchType = “”;
Random oRandom = new Random();
boolean bSwitch = oRandom.nextBoolean();

if (bSwitch) strBatchType = “Type A”;
else strBatchType = “Type B”;

startBatch(strBatchType);
Thread.sleep(2000);

// Fake an issue when Batch Type is “Type B”, pause for 3s.
private static void doThis(String strBatchType)
{
  System.out.println(“Now doing this….”);
  if (strBatchType.equals(“Type B”))

try
{
  Thread.sleep(3000);
}
catch (Exception e){}

System.out.println(“——————“);
}
```

First, let’s run the JAR without Dynatrace to prove it works: `java -jar DTBasicsCreatingMeasures.jar`

Now instrument it with the `-agentpath` parameter you received when you setup your agent tier.

No idea what I’m talking about? Read [this tutorial](https://agardner.net/batch-job-monitoring-dynatrace/) to understand how to instrument your JAR.