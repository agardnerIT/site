---
layout: post
title: Invalid dylib load Python Error
categories: [python, openssl]
---

Here's how I fixed the `Invalid dylib load. Clients should not load the unversioned libcrypto dylib as it does not have a stable ABI` error on MacOS.

Recently I moved from the MacOS standard (old) terminal to `zsh`. I also updated all my `brew` packages. I'll be honest, I don't know which of those two things caused the issue, but the end result was that most of my Python-based programs were broken with the error report:

```
Invalid dylib load. Clients should not load the unversioned libcrypto dylib as it does not have a stable ABI
```

After some hunting, I found the solution.

1. Open a new terminal window and `cd` to `/usr/local/opt`
2. List all directories which begin with 'openssl': `ls | grep '^openssl*'`. I get `openssl` and `openssl@1.1`
3. Set the `DYLD_FALLBACK_LIBRARY_PATH` variable to point to the `lib` folder of the `openssl` directory. Note: I chose the `openssl@1.1` directory. Frankly that was just a guess. I'm not claiming that's correct!
```
export DYLD_FALLBACK_LIBRARY_PATH=/usr/local/opt/openssl@1.1/lib
```
4. Open a new terminal window and retry your script. It should now work.

As always, if you have any comments or suggestions, please do not hesitate to [contact me](contact).
