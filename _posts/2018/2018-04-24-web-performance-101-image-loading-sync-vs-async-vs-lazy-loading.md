---
layout: post
title: Web Performance 101 - Image Loading (Sync vs. Async vs. Lazy Loading)
header_image: /images/headerimages/web-perf101-image-loading-header.png
categories: [web performance]
---

Let’s examine the difference to your users (and your server bill) between various image loading strategies. We’ll compare “standard” synchronous loading vs. asynchronous vs. lazy loading with the new `IntersectionObserver` API.

The modern web is **heavily** dependent on images. I don’t think that’s news to anyone. As such it’s worth considering your strategy when loading heavy content such as images or video.

Sending content that is too heavy (in terms of MB) is bad for many reasons, here are 4:

- Slow down your website performance.
- Annoy your users – your site is slow and it’s eating all their bandwidth.
- Waste your money – you’re spending money on unnecessary infrastructure / third parties just to deliver and support your massive files.
- Destroy your search engine rankings.

As with most things, there’s a balance to be struck. Usually this is a tripartite discussion between marketing (who want the highest possible content quality), web developers (who want the lowest allowable quality to improve page load speed) and business (who want to make money & don’t necessarily care how that’s done).

How do we strike an acceptable compromise between these three competing interests and ensure that you’re getting the best balance? Here are a few steps which I’d attack in this order:

## Resize Your Images

Modern digital cameras will produce images thousands of pixels square. 99% of the time these are inappropriate for directly uploading to a website. Your screen is a thousand pixels square at most. If you’re know the physical pixel size of an image (say 250x250px for an icon) – why bother loading a 2500x2500px image?

You’re sending (and paying for) 10x the amount of data to be sent to the user. The user’s browser then has to spend time resizing it down to 250×250 anyway. A total waste of time.

> Reduce the physical size of your images wherever appropriate. **Especially** for mobile-focused websites.

## Optimise Your Images

There are various online websites offering image optimisation these days. One I particularly like is [TinyPNG](https://tinypng.com).

Using [this image](https://unsplash.com/photos/mBHuEkka5wM) from Adrien Ledoux, TinyPNG shrunk the image from `1.2MB` to `367KB` (a 70% reduction) and I can’t see any difference in quality.

> Sites like TinyPNG can shrink images by as much as 90% with no discernible loss of quality.

## Load Your Images Appropriately

So, by now your images are an appropriate physical (pixel) size and you’ve optimised them to get the best balance of quality and size.

How you deliver images to your end users is critical. Let’s investigate 3 possibilities...

> How you deliver images to your end users is a critical factor. It’ll save you money, improve your search engine rankings and make for happier customers.

## Synchronous Loading

This is the standard, default solution. Just include an `<img>` tag on your page. The page will load top-down, in order, which means large images will block the rest of the content (text) until they’re finished.

I created a large (13.6MB) dummy page, loaded it & recorded the timings from Chrome DevTools:

| Connections | Size (MB) | Finish | DOMContentLoaded (ms) | Load (ms) |
|----|----| ----- | ------| ----- |
| 7 | 13.6MB | 4.18s | 356ms | 4.01s |