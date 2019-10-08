---
layout: post
title: Version Controlled and Automated Syntheric Scripts
header_image: /images/headerimages/vc-synthetic-scripts-header.jpg
categories: [automation, devops, synthetic]
---

If only there was a way to version control and automate the creation and deployment of Dynatrace Synthetic scripts. Well, I’ve got good news for you…

I’ve recently been working with a large DevOps customer who, like many, want everything-as-code so that it can be audited, automated and version controlled. They love the [Dynatrace Synthetic](https://www.dynatrace.com/capabilities/synthetic-monitoring) robot and it’s capabilities but they needed a way to specify these scripts as code rather than relying on the Dynatrace GUI to record and edit these scripts.

Luckily for them, the clever minds in the Dynatrace development team have already thought of this and so we can create, store and edit synthetic scripts as JSON files.

## What's a Synthetic Script, Anyway?

Before we get into how to do this, it’s worth recapping exactly what a synthetic script is and how it’s formed.

- A synthetic script is a user journey. It has multiple steps.
- Each step can have one (or more) actions (wait for time / wait for text / click / form field input etc.)

An example might be a journey in which does the following:
- Navigate to the homepage.
- Click on Sign In. Enter their username and password. Click Submit.
- Once logged in, click another link.
- Click logout and wait for the logout message to be shown.

## Sample JSON Journey

Here’s a [sample user journey defined as a JSON file](https://github.com/agardnerIT/OddFiles/blob/master/adamgardner.co.uk_Contact_Form_Synthetic_Script.json). The structure is fairly straightforward in that there is an array of steps and within each step, there is an array of actions.

This script:
1. Navigates to my homepage, waits for the page to load then waits until the text Posted is found.
2. Clicks the about me link, waits for the page to load then waits until the text About Me is found.
3. Clicks the contact me link, waits for the page to load then completes and submits the contact form.
4. After submission, the robot waits until the text Thank you for your message is displayed.

## Store in VCS

Go ahead, store that in your favourite version control system. Then when you’re ready, just upload to the synthetic portal as you would with any other Dynatrace Synthetic script. Easy!

## Go Forth and Monitor Synthetically

I hope this post has demonstrated how easy it is to integrate Dynatrace Synthetic monitoring into your automated testing pipelines so now there really is no excuse for “well it worked in Dev”, is there!?
