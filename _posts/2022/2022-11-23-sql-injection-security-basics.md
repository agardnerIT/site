---
layout: post
title: "SQL Injection: Security Basics"
categories: [sql, sql injection, security]
header_image: /images/headerimages/sql-injection.png
---

What is a SQL Injection? How is one performed? How can you mitigate against these attacks?

# Introduction

Despite being 48 years old, SQL is still going strong. Also still going strong is the SQL injection ([OWASP has this at third spot on their vulnerabilities list for 2021](https://owasp.org/Top10/A03_2021-Injection/)). 48 years and we're still suffering from this!

# Live Demo
[Here is a live demo tutorial](https://killercoda.com/agardnerit/scenario/security-sql-injection) hosted on Killercoda which walks you through this post with a hands-on demo.

# What is a SQL Injection?
A SQL injection (or really any kind of [Injection attack](https://owasp.org/Top10/A03_2021-Injection/)) occurs primarily because the developer has trusted the user input and passed it straight to the backend - in this case, the SQL database.

When a user is allowed to pass input directly into a backend, inevitably "bad" users will attempt to abuse this trust and make the program (in this case the database) run something it "shouldn't".

It's important at this point to note that the SQL being passed is technically "valid". The SQL engine sees that it is a valid command and tries to run it.

That said, what a language parser / program considers "technically valid" is not at all what a human (i.e. the developer) may call "valid".

For example, imagine a program asks you to enter the last name (surname) of a user to retrieve their details.

You enter `Bloggs` and the input is taken and used to formulate this SQL statement:

```
SELECT Address FROM Accounts WHERE LastName='Bloggs'
```

Nothing wrong with that and nothing nefarious either.

Now instead of `Bloggs`, enter `fake' OR true;--`

Suddenly the application returns **all** user details, not just `Bloggs`.

## Why Did This Happen?

Look again at the first SQL statement. Your input is passed into the `WHERE` clause.

So the second (dangerous) SQL statement is:

```
SELECT Address FROM Accounts WHERE LastName='fake' OR true;--'
```

If LastName is `fake` then why does it even work? Surely the DB doesn't contain anyone with the surname `fake`? No, but let's break that SQL statement down...

```
SELECT Address FROM Accounts WHERE LastName='fake'
```

That part is valid SQL and you're correct that no-one has the surname `fake`. So far, so good.

`OR` is a valid SQL keyword and `true`. Well, `true` is always going to be `true` right?

So in effect you're saying: "Give me all addresses where the LastName is fake or yes". Since SQL interprets the "or yes" to always true then in effect, every user in the database will match that last part and will be included for you.

The final parts of the statement: `;--` are some SQL magic. The `;` means "end the line here", but remember we have that pesky extra `'` to deal with (the counts of which always need to match). Lucky for us, `--` in SQL means "ignore everything afterwards".

So in the end, we end up with an effective SQL statement of:

```
SELECT Address FROM Accounts WHERE LastName='fake' OR true;
```

We now know that, due to the `OR true`, this will **always** match and thus you get every Address in the database.

## Contrived Example?

At this point, you might think this is a simplified and contrived example only dreamt up in order to create a blog post.

You might reasonably point out that many frameworks _attempt_ to protect against SQL injection attacks automatically. You may also say (correctly) that all input should be validated.

I agree with you, everything above **is** true.

But if this is _so easy_ to avoid, why is it still the 3rd most popular vulnerability in 2021 according to OWASP?

Precisely **because** this is so simple means it is pervasive.

# Prevention

How can you prevent SQL injections?

1. Never trust user input and do not attempt to "sanitise" input. Always positively validate input. If it looks "fishy", throw it away. Do not try to "make sense" the input.
2. Use available tools like frameworks that attempt to check for SQL injections.
3. Use controls like `LIMIT` to slow down or prevent mass data breaches if you are victim to an attack.
4. Some commercial and open source tools offer on-the-fly runtime SQL injection blocking (like [Dynatrace](https://dynatrace.com))

More details available via [OWASP](https://owasp.org/Top10/A03_2021-Injection/#how-to-prevent).

_Title image credit: Photo modify by Photo by [Diana Polekhina](https://unsplash.com/@diana_pole) on [Unsplash](https://unsplash.com/s/photos/injection)_


