---
layout: post
title: "Dynatrace Basics: Business Transactions"
permalink: dynatrace-business-transactions
categories: [business transactions, dynatrace, appmon]
---

As a follow up to the previous [Creating Measures](dynatrace-basics-creating-measures) tutorial, let’s introduce another key Dynatrace Application Monitoring (AppMon) concept: Business Transactions.

**NOTE: THIS TUTORIAL REFERS TO THE LEGACY APPLICATION MONITORING PRODUCT FROM DYNATRACE NOT THE DYNATRACE PLATFORM.**

In the last tutorial, we saw how to create basic datapoints for long term trending purposes. These are perfect as they’re extremely low overhead in terms of the processing and storage requirements on the AppMon system. However, they do have limitations.

> A Business Transaction is a way to combine multiple measures to form more complex conditions.

## Measures vs. Business Transactions

| Measures | Business Transactions (BTs) |
|----------|--------------------------|
| Simple   |    More Complex |

Low Overhead	Higher Overhead
Purepath Data: Not Linked	Purepath Data: Linked
Handles Simple Logic	Handles Complex Logic
> Measures are great for simple business requirements such as response time or SLA tracking. Business Transactions are the best fit for more complex business-logic modelling.