---
layout: post
title: Access Any Deactivated Facebook Account Without a Password
header_image: /images/headerimages/facebook-without-password-header.jpg
categories: [facebook, security]
---

It turns out that Facebook want to maintain your ~~data~~ custom so badly that they’ll even invite you to login without needing your password! Let me explain...

## Scenario

You create a Facebook account which is attached to your email address. Let’s say `john@johndoe.co.uk`. For whatever reason you then decide you don’t want the FB account and domain anymore – so you deactivate the Facebook account and let the domain expire. Fine, right? All sorted!

## The Problem

Someone new comes along and registers your domain name doe.co.uk and because their name is also john, their email address is also `john@johndoe.co.uk`. They attempt to sign up Facebook with their email address but they can’t – because it’s already attached to the old person’s account.

So far, so good? That’s perfectly normal behaviour.

**What’s not normal however, is what happens next...**

Facebook take it upon themselves to send an email which includes a **link to login without a password**.

![]({{ site.baseurl }}/images/postimages/facebook-without-password-1.png)

Now, I’ve got full access to this user’s account, all their private messages, all their photo’s. In essence, I *am* them.

![]({{ site.baseurl }}/images/postimages/facebook-without-password-2.jpg)

## Even Worse News...

You’ll probably have noticed the “Sign In with Facebook” buttons around the web. Great for convenience – not so great now though huh? I have full access to this user’s account on tens of thousands of services. Including:

- Spotify
- Instagram
- Vimeo
- Groupon
- Disqus
- Change.org

## The Fix

I understand that Facebook does not control the internet (some may argue with that statement) and that they have no control over how, when and why domain names get registered. But they do have access to their systems and processes.

The fix for this is incredibly simple:
– Facebook should **delete** my account, not indefinitely deactivate it.
– Facebook shouldn’t, ever ever send an email with a link to login without a password. Ever.

## Disclaimer

I have reported this vulnerability / bug to Facebook via their [bug bounty program](https://www.facebook.com/whitehat). They do not see this as bug or an issue. I followed their guidelines and did not disclose this until they’ve actually closed my report.

I was so concerned about this that I queried it with them twice and have been told by two separate Facebook employees that it’s nothing to worry about.

I am not a security researcher or hacker. I have no intrinsic interest in security vulnerabilities or exploits. I’m just like you, extremely concerned about this.

I’ve approached each of the companies listed above to ask for their comments and will update if / when they respond.