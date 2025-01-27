---

title: Build a Web Scraper with jq and pup
categories:
- webpage scraper
- webpage parser
- linux
- jq
- pup
date:
  created: 2021-03-16
---

Recently I wanted to build a rudimentary webpage scraper which would run from the command line.

<!-- more -->

As I progressed I noticed myself having to extensively `grep`, `cut` and stitch bits and pieces of logic together.

One of my rules is that if the activity you're attempting seems fairly standard, someone has probably already done it or at least made utilities to make the activity easier. They've probably put more time and effort into it than you have & thus it's better than your effort would be. Don't reinvent the wheel.

This led me to two linux libraries: `pup` and `jq`.

`pup` is a handy HTML parser for the command line and `jq` is the equivalent JSON parser.

By combining these two utilities, it was very easy to achieve my goal without lines and lines of convoluted code.

## Scenario

Say I want to extract some information from this page: `https://agardner.net/serverless-voting/`. Take a look at the source code of that page and you'll see standard HTML text like this:

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Begin Jekyll SEO tag v2.7.1 -->
    <title>Serverless, Zero Database Voting System | Adam Gardner</title>
    <meta name="generator" content="Jekyll v3.9.0"/>
    <meta property="og:title" content="Serverless, Zero Database Voting System"/>
    <meta name="author" content="Adam Gardner"/>
```

You'll also see `<script>` tags, one of which looks like this:
```javascript
<script type="application/ld+json">
    {
      "@type":"BlogPosting",
      "@context":"https://schema.org"
      "headline":"Serverless, Zero Database Voting System",
      "dateModified":"2020-06-14T00:00:00+00:00",
      "datePublished":"2020-06-14T00:00:00+00:00",
      "mainEntityOfPage":{
        "@type":"WebPage",
        "@id":"https://agardner.net/serverless-voting/"
      },
      "author":{
        "@type":"Person",
        "name":"Adam Gardner"
      },
      "url":"https://agardner.net/serverless-voting/",
      "description":"I needed a voting system for this website which was compatible with serverless pages. I also wanted it to be zero-login which ruled out using a third-party plugin. The result was a serverless, zero database &amp; zero login voting system using AWS. Here is how…"
    }
</script>
```

In this scenario, I want to extract the content of the `<title>` tag and then extract the content of the `datePublished` field from this JSON snippet.

## Install both libraries

```
pip install jq
```

Depending on your platform, `pup` can be installed in different ways. Easiest is to use `go get` or `brew`.

```
go get github.com/ericchiang/pup
OR
brew install pup
```

Alternatively, see instructions on the [releases page](https://github.com/ericchiang/pup/releases).

If all is successful, these two commands should provide output:

```
jq --version
pup --version
```

## Extracting Title
Remember that I want to do this via a command line script, so create a new file in `/tmp` called `scraper.sh`. 

Make it executable:
```bash
chmod +x /tmp/scraper.sh
```

Paste the following content:

```
#!/bin/bash
curl $URL
```

Now set the URL value and call the scraper.sh:

```
URL=https://agardner.net/serverless-voting/ /tmp/scraper.sh
```

Notice that it prints the entire HTML content and we only want the `<title>` tag so modify `scraper.sh` to look like this:

```bash
#!/bin/bash
title=$(curl $URL | pup 'title')
echo $title
```

Here we're piping the output of curl to the `pup` command and asking `pup` to print only the `<title>` tag.

The output should look like this:

```bash
% URL=https://agardner.net/serverless-voting/ /tmp/scraper.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 24491  100 24491    0     0   254k      0 --:--:-- --:--:-- --:--:--  254k
<title> Serverless, Zero Database Voting System | Adam Gardner </title>
```

Let's clean that up a bit. Modify the `/tmp/scraper.sh` file as such that we add the silent (`-s`) flag to the curl command. Adding this flag means we don't see the download stats bar.

Then add the `text{}` modifier to the `pup` command. This tells `pup` that we only want to see the text of the tag, not the actual start and end tags themselves.

Your script should now look like this:

```bash
#!/bin/bash
title=$(curl -s $URL | pup 'title' text{})
echo $title
```

Re-run and you should see this output:

```bash
% URL=https://agardner.net/serverless-voting/ /tmp/scraper.sh
Serverless, Zero Database Voting System | Adam Gardner
```

## Extract Date Published

Recall that there's a block of JSON in the source code which contains the information we need:

```javascript
<script type="application/ld+json">
    {
      "@type":"BlogPosting",
      "@context":"https://schema.org"
      "headline":"Serverless, Zero Database Voting System",
      "dateModified":"2020-06-14T00:00:00+00:00",
      "datePublished":"2020-06-14T00:00:00+00:00",
      "mainEntityOfPage":{
        "@type":"WebPage",
        "@id":"https://agardner.net/serverless-voting/"
      },
      "author":{
        "@type":"Person",
        "name":"Adam Gardner"
      },
      "url":"https://agardner.net/serverless-voting/",
      "description":"I needed a voting system for this website which was compatible with serverless pages. I also wanted it to be zero-login which ruled out using a third-party plugin. The result was a serverless, zero database &amp; zero login voting system using AWS. Here is how…"
    }
</script>
```

From this JavaScript snippet we need to extract the `datePublished` field:

```
"2020-06-14T00:00:00+00:00"
```

Adjust your `scraper.sh` file to look like this:

```bash
#!/bin/bash
page_html=$(curl -s $URL)
title=$(echo $page_html | pup 'title' text{})
echo $title
```

All we've done here is store the output of the `curl` command into a variable called `page_html` so we can manipulate and query the HTML without repeated `curl` calls to the website.

Use `pup` to extract the `<script type="application/ld+json">` tag. Modify your `scraper.sh` again:

```bash
#!/bin/bash
page_html=$(curl -s $URL)
title=$(echo $page_html | pup 'title' text{})
date_published=$(echo $page_html | pup 'script[type="application/ld+json"] text{}')
echo $title
echo $date_published
```

This _sort of_ works but it outputs the title then entire JSON object which isn't quite what we want:

```
% URL=https://agardner.net/serverless-voting/ /tmp/scraper.sh
Serverless, Zero Database Voting System | Adam Gardner
{"@type":"BlogPosting","headline":"Serverless, Zero Database Voting System","dateModified":"2020-06-14T00:00:00+00:00","datePublished":"2020-06-14T00:00:00+00:00","mainEntityOfPage":{"@type":"WebPage","@id":"https://agardner.net/serverless-voting/"},"author":{"@type":"Person","name":"Adam Gardner"},"url":"https://agardner.net/serverless-voting/","description":"I needed a voting system for this website which was compatible with serverless pages. I also wanted it to be zero-login which ruled out using a third-party plugin. The result was a serverless, zero database &amp; zero login voting system using AWS. Here is how…","@context":"https://schema.org"}
```

We need to take this JSON output and pass it to `jq`. JQ is a JSON parser. It works like so:

```
some input text | jq 'some_desired_output'
```

The most basic would be to just ask for the entire input document back as output. The `.` character is the shorthand for this. Run the following in a terminal window

```bash
echo '{"foo": "bar"}' | jq '.'
```

You should see a pretty printed JSON object as output:

```bash
%  echo '{"foo": "bar"}' | jq '.'
{
  "foo": "bar"
}
```

After the `.` you can request any JSON field. So to get `"bar"` as the output, do this:

```bash
echo '{"foo": "bar"}' | jq '.foo'
```

You'll see:

```
% echo '{"foo": "bar"}' | jq '.foo'
"bar"
```

We can use this concept in our script so after we've used `pup` to retrieve the `<script>` tag, we will use `jq` to retrieve only the `datePublished` JSON field.

Modify `scraper.sh` as follows:

```bash
#!/bin/bash
page_html=$(curl -s $URL)
title=$(echo $page_html | pup 'title' text{})
date_published=$(echo $page_html | pup 'script[type="application/ld+json"] text{}' | jq '.datePublished')
echo $title
echo $date_published
```

So we're echoing the `page_html` content then using `pup` to extract just the `<script type="application/ld+json">` block. Then we're passing that extracted value to `jq` and asking for the `datePublished` value. Which gives us:

```bash
RL=https://agardner.net/serverless-voting/ /tmp/scraper.sh
Serverless, Zero Database Voting System | Adam Gardner
"2020-06-14T00:00:00+00:00"
```

One final (optional) cleanup step would be to remove the quotation marks. That's as easy as adding the `-r` flag to `jq`. As `jq --help` suggests:

```
-r    output raw strings, not JSON texts;
```

So:

```
#!/bin/bash
page_html=$(curl -s $URL)
title=$(echo $page_html | pup 'title' text{})
date_published=$(echo $page_html | pup 'script[type="application/ld+json"] text{}' | jq -r '.datePublished')
echo $title
echo $date_published
```

Prints this:

```bash
URL=https://agardner.net/serverless-voting/ /tmp/scraper.sh
Serverless, Zero Database Voting System | Adam Gardner
2020-06-14T00:00:00+00:00
```

