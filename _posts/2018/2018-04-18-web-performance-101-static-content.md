---
layout: post
title: Web Performance 101 - Static Content
categories: [web performance]
---

You may have heard of static content, but what difference does it really make to web performance? Let’s find out...

## What Is Static Content?

WHAT IS STATIC CONTENT?

Simply put, it is content (words, text or more accurately HTML content) that doesn’t change.

In reality, this means that all users (or most users) will receive that same content each time they load the page. Think about blog posts, news articles or tutorials – things that will rarely change once they’ve been published. It doesn’t mean it never changes – you can always edit the static pages and upload them again.

The opposite of static content is dynamic content. That is, content that changes each time the page is reloaded. Think about search result pages or online catalogues. There is another mechanism which can handle dynamic pages – caching… More about this in a future post…

So, what difference will it make to serve exactly the same page via a static file vs. the standard dynamic method?

## Test It

This site is hosted on WordPress with an Apache webserver and a MySQL database. Every time a user requests a page, the Apache server needs to pull the data from the database, via a layer of PHP. That’s not to mention the imagery and any third party scripts. Each layer adds time to serve this request.

To test dynamic vs. static content, we’ll:

- Use an identical webpage
- Hosted on an identical server
- Served via the same domain name
- We will not alter the images, where or how they’re served.
- We will not alter / remove any third party tags or how they’re served.

## Dynamic Content

I’ll use [this post](/monitor-digitalocean-lamp-stack-dynatrace/) which is a fairly long, image heavy post.

## Static Content

I’ll save the source code of the same page as a static `.html` page.

## Raw Values for Dynamic Page

All values in milliseconds.

| Finish | DOMContentLoaded | Load |
|--|--|--|
| 1230 | 1003 | 1230 |
| 1270 | 1003 | 1280 |
| 1330 | 1006 | 1330 |
| 1190 | 984 | 1190 |
| 1350 | 1120 | 1350 |
| 1240 | 992 | 1240 |
| 1190 | 912 | 1200 |
| 1170 | 991 | 1180 |
| 1270 | 1001 | 1270 |
| 1280 | 1006 | 1280 |


## Raw Values for Static Page

| Finish | DOMContentLoaded | Load |
|--|--|--|
| 915 | 721 | 916 |
| 936 | 730 | 937 |
| 888 | 694 | 889 |
| 933 | 724 | 934 |
| 892 | 681 | 894 |
| 874 | 686 | 875 |
| 950 | 759 | 952 |
| 866 | 668 | 870 |
| 936 | 697 | 942 |
| 899 | 697 | 900 |

## Dynamic Summary

| | Finish | DOMContentLoaded | Load |
| Average | 1252ms | 1002ms | 1255ms |
| Standard Deviation | 59.78 | 50.11 | 57.59 |

## Static Summary

| | Finish | DOMContentLoaded | Load |
| Average | 909ms | 706ms | 911ms |
| Standard Deviation | 29.12 | 27.30 | 29.33 |

> By every metric, the static page is significantly faster.

  Static page response time 27% faster than the dynamic page.

  Static page = much lower standard deviation. It’s faster, more often and more reliably.

As an added bonus, going "static" can open you up to possibility of serving sites via serverless infrastructure such as AWS S3.

Not only is it better for the environment (you’re using less electricity and resources), its better for your productivity (#NoOps anyone) but it’s better for your bottom-line too! You only pay for what you use.