# Why This Blog Went Serverless

I've recently moved this blog from Wordpress hosted on a DigitalOcean hosted virtual machine to GitHub Pages, a "serverless" hosting platform. In this post, I aim to explain my reasoning.

I'll share some tangible results in a future post.

First though, some facts that are pertinent to consider when reading this post:

- This is a personal site. It's not mission critical. It's not the end of the world if it's unavailable.
- I don't process transactions or capture any financial user information on this site.
- For practical purposes, most of the content can be considered static. It may change from time to time, but 99% of the content remains the same once published. There's very little need for a database as most content can be served perfectly well via static files.
- Running this site is not my day job. I need it to "just work".

> "Serverless" is one tool in your toolbox, Not a panacea.

## Considerations & Choices
Like any major architectural shift, the benefits and costs need to be carefully weighed. Although this site is small by most standards, there was still a fair amount to consider:

### Lift & Shift vs. Rewrite
GitHub Pages is powered by [Jekyll](https://jekyllrb.com). If it's good enough for GitHub, it's good enough for me. Jekyll is written in markdown & Liquid templating format. So some conversion will be necessary from Wordpress to Jekyll.

Jekyll offers an [importer](http://import.jekyllrb.com) for most common blog / CMS platforms. You give the importer your database connection info, the importer does all the hardwork by translating the Wordpress into Jekyll ready content.

#### Choice: Rewrite
I chose **not** to utilise the import feature. Instead I took the opportunity to use a new blog template - one specifically designed for Jekyll.

I also reworked all of the posts into Jekyll-native markdown format.

Reasoning: A template specifically designed for Jekyll is more likely to be more **compatible** and **lightweight**. Markdown format is easy to read, store and is **transferable** - so if I decide to move away from GitHub Pages, all I need to do is copy my plain text markdown formatted files. No more database exports / imports.

### Backups & Maintenance
Using a "serverless" platform, there is no infrastructure for me to manage. Of course, there is a server somewhere, but that's GitHub's problem, not mine.

This means I can focus on writing content & not worry about updating infrastructure. In fact, I forgot to upgrade a Wordpress instance I use on a demo domain - it was promptly hacked & used for essay writing posts.

GitHub Pages relies on GitHub. In other words, it's a fully functional version control system, which also functions as a handy backup tool. I can version control and rollback to any previous version of my blog post, all hosted & managed by GitHub.

### Cost
Being "serverless", means no servers to pay for. The GitHub Pages service is free. Other "serverless" hosting solutions such as AWS S3 are free or extremely low cost too.

Result: My hosting costs just reduced to almost zero (aside from domain name renewal).

### Scale
Serverless solutions will scale with your traffic. That is all handled and managed by the provider. No more worrying about load balancers, number of VMs, scaling etc. All I do is provide my content and they figure out the rest.

### Environmental Impact
This one is harder to measure, but I like the idea that by reducing my VM usage, in a tiny way, I'm reducing my environmental impact. This cannot be a bad thing. 

Imagine the amount of severely underutilised infrastructure components running in datacentres today. The environmental impact of a single VM is tiny, but multiply that many millions of times - it all adds up. As [one example](https://digiconomist.net/bitcoin-energy-consumption), processing a single Bitcoin transaction contributes the same CO2 as 750,000 VISA transactions!

> 1 Bitcoin transaction equates to the same CO2 consumption as 750,000 VISA transactions.

## Issues / Concerns

Serverless delivery systems offer one significant downside: There is no server when means no way to run server side code or logic.

Case in point: The contact form.

### Migrating the Contact Form
In the old Wordpress virtual machine setup, I had an HTML form which sent data to the webserver on the VM. PHP running on the VM processed this information and sent me an email with the contact form details. All very simple and standard.

In the new world, I have no native capability to run any server side code. I can create the contact form, but that's all.

#### Possible Solutions
There are two potential solutions that spring immediately to mind:

1) Create a VM for contact form processing.
2) Use serverless functions to process the form.

#1 is pointless. There is zero value in creating a VM only to process the contact form. If I do that, I might as well host the whole site _on_ that VM and move back to Wordpress.

#2 looks promising as serverless functions only run when they're actually in use. Saves money and the environment.

I'll write a seperate post on how I redesigned the contact form to be serverless, but it really wasn't that difficult (once I got over the AWS learning curve).

## Lessons Learned

### Consider Your Scenario
As I said at the top of the article, serverless is not actually serverless. Serverless also is not a panacea. Serverless will not be the right fit for everyone.

Take the time to fully evaluate **your** situation, and the effort involved in a move. *Then* you'll be in a position to make an informed decision.

### New Technologies
Don't be afraid of new technologies. Generally speaking, newer technologies and methodologies offer a better or more efficient way of doing things. Don't be closed-minded. Don't ignore a potentially excellent solution, just because it is scary and takes a little bit of time to get your head around.

> Embrace new technology & methodologies. There are good reasons why we're not all still flying in the Wright Brothers planes.

### Take Time & Practice
Like everything in life, it takes time to figure things out. That's fine. Take your time, experiment, break things, take time to understand how and why things are working the way they are.

The time spent practicing and understanding new tools will pay dividends later.

### Benefits are Worth It
When all is said and done, in my case, the benefits of the move have been worth it:

- The site structure is much more lightweight, cleaner and easier to maintain.
- I have a ready made backup & restore solution via GitHub.
- I have slashed my response times (more on that in a future post).
- I have vastly reduced my risk of being hacked or attacked - all infrastructure and DDOS protection is managed by GitHub. All blog posts are open source - they're really nothing to hack.
- I have embraced new tech so that I now get instant push notifications on my phone for contact form submissions.
- I'm not paying for infrastructure.

I hope this post has given you some pointers and thoughts about a potential move to serverless.

As always, if you have any comments or suggestions, please do not hesitate to [contact me](contact).