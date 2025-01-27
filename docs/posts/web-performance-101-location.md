---
layout: post
title: Web Performance 101 - Location
categories:
- web performance
- geolocation
date:
  created: 2018-04-11
---

How much does server location influence the performance and response time of your website?

**A lot...**

<!-- more -->

Performance professionals have a habit of diving in at the deep-end of a problem. Immediately talking about JVM heap sizes and concurrent thread counts. This is often perfectly valid. However, it really does pay not to forget the basics.

## Location, Location, Location

As they say, location is everything. In the physical world and the digital. It’s logical if you think about it.

If I asked you to go walk to the shop and back, it’d take you longer if the shop was far away vs. if it was just around the corner. That’s logical since we can only move at a certain speed.

Since everything in the universe (as far as we know) abides by the laws of physics, websites (more accurately the bits and bytes that make them) are similarly constrained.

> It’ll take longer to serve your site from somewhere geographically remote to your users than somewhere geographically near.

It all comes down to where your users are located in relation to your server. The closer these two things are, the faster the bits and bytes of your site will get to them.

## Prove It

I’ve created 3 indentical WordPress droplets using DigitalOcean.

- The user (client) is in London, UK.
- Droplet #1 is hosted London, UK.
- Droplet #2 is hosted in New York, USA.
- Droplet #3 is hosted in San Francisco, USA.
- All 3 are hosting the stock WordPress theme image with nothing added on a $5 droplet.
- I’ll be measuring the performance with Chrome DevTools, ensuring I’ve got **Disable cache** clicked.
- Each page load is executed 10 times per location.
 

## Raw London Values

All values in milliseconds.

| Finish | DOMContentLoaded | Load |
|--------|------------------|------|
| 564    | 537              | 644  |
| 540    | 528              | 603  |
| 578    | 549              | 686  |
| 609    | 591              | 690  |
| 631    | 615	            | 706  |
| 575    | 567	            | 644  |
| 585    | 570	            | 662  |
| 584    | 557	            | 662  |
| 641    | 594	            | 704  |
| 573    | 548	            | 653  |
 
## London Summary

|                    | Finish | DOMContentLoaded | Load    |
|--------------------|--------|------------------|---------|
| Average            | 588ms  | 565.6ms          | 665.4ms |
| Standard Deviation | 30.73  | 27.50            | 31.89   |

## Raw New York Values

All values in milliseconds.	

| Finish  | DOMContentLoaded | Load |
|---------|------------------|------|
| 756     | 700              | 785  |
| 1008    | 1000             | 1200 |
| 927     | 796              | 929  |
| 1008	  | 951              | 1008 |
| 952     | 822              | 957  |
| 952     | 846              | 954  |
| 981     | 852              | 983  |
| 1100    | 1009             | 1160 |
| 947     | 860              | 949  |
| 997     | 799              | 999  |
 
## New York Summary

|                    | Finish   | DOMContentLoaded | Load    |
|--------------------|----------|------------------|---------|
| Average            | 962.8ms  | 863.5ms          | 992.4ms |
| Standard Deviation | 87.52    | 97.23            | 117     |


## Raw San Francisco Values

All values in milliseconds.

| Finish | DOMContentLoaded	| Load |
|--|--|--|
| 1570	| 1140	| 1570 |
| 1520 | 1100 | 1520 |
| 1510 | 1007 | 1510 |
| 1500 | 1005 | 1500 |
| 1580 | 1130 | 1580 |
| 1470 | 1130 | 1480 |
| 1510 | 1140 | 1510 |
| 1530 | 1120 | 1530 |
| 1540 | 1160 | 1540 |
| 1480 | 1100 | 1480 |

## San Francisco Summary

| |	Finish | DOMContentLoaded | Load |
| Average | 1521ms | 1103ms | 1522ms |
Standard Deviation | 35.42 | 54.34 | 33.93 |

> For a London-based user, serving exactly the same site from San Francisco takes nearly 159% longer than London.

> The consistency of response time drops due to the unreliability of the internet – you’re more likely to get a bad response time, more often.

