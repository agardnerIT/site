---
layout: post
title: "OpenTelemetry Instrumented Python FastAPI"
categories: [opentelemetry, instrumentation, tracing, python, fastapi]
header_image: /images/headerimages/instrumented-flaskapi.jpg
---

What is OpenFeature and why might you need it?

# What Is OpenFeature?

[OpenFeature](https://openfeature.dev) is an open, vendor-neutral specification for feature flagging (FF). It provides a standardised abstraction layer between your code and the underlying feature flag vendor.

# What Problems Does OpenFeature Solve?

## OpenFeature Benefits for Feature Flag End Users

Imagine you wish to integrate with a feature flagging solution from `vendorA`. You code needs to communicate with `vendorA` using their APIs and their specific code. In other words, your code is tightly coupled to that one vendor. If you want to move to a new vendor - it's a lot of work.

How about different parts of the organisation using different vendors? Scale the above scenario up and you'll understand the issue.

What if you need to use multiple feature flag vendors at the same time? OpenFeature provides "federated" options so you can ask for flag `foo` and the provider that has it, returns it.

This is not just an IT benefit either, the ability to use the "best of breed" feature flag tool (and be able to quickly switch) offers business agility and can expedite time to market.

## OpenFeature Benefits for Feature Flag Vendors

As a feature flag vendor, you want to encourage ways for potential users to easily trial and adopt your solution. Most likely, you also want to "play nice" with other vendors - no-one likes vendor lock-in.

OpenFeature provides that opportunity so it is in all feature flag vendors interests to widely adopt OpenFeature.

# How Does OpenFeature Work?

Rather than directly connecting your code to the feature flag vendor, your code instead interacts in a standard way with the OpenFeature API. Vendor `providers` translate that code into the vendor specific API calls.

Switching vendors is a one line code change: `set_provider(VendorAProvider())` becomes `set_provider(VendorXProvider())`.

```
# Set which provider to use
open_feature_api.set_provider(VendorAProvider())

# Get a String flag called `foo`
open_feature_client.get_string_details(key="foo", default_value="missing_flag")
```

![openfeature_direct](/images/postimages/openfeature_direct.jpg)
![openfeature_new](/images/postimages/openfeature_new.jpg)

## What Exactly is a Provider?

A provider is the "translation" code between the OpenFeature API (see above) and the vendor specific calls.

The provider is responsible for calling hte vendor and returning the flag in an OpenFeature compliant way.

## Who Writes Providers?

Vendors usually write the providers but you can also create your own.

Providers can be written in any language. For example, here is the [Split.io JavaScript Provider](https://github.com/splitio/split-openfeature-provider-js)

## OpenFeature Hooks

The OpenFeature spec offers [the concept of hooks](https://docs.openfeature.dev/docs/reference/concepts/hooks) which, as it sounds, is a way to hook into feature flag execution during runtime.

Hooks can fire on one or more of these lifecycle stages:

- [Before](https://docs.openfeature.dev/docs/reference/concepts/hooks/#before)
- [After](https://docs.openfeature.dev/docs/reference/concepts/hooks/#after)
- [Error](https://docs.openfeature.dev/docs/reference/concepts/hooks/#after)
- [Finally](https://docs.openfeature.dev/docs/reference/concepts/hooks/#after)

Need to notify that a flag has been toggled? Use the `After` hook.

Want to potentially prevent a hook if it has been approved? The `Before` hook might be what you're looking for.

Need to fix something if a FF toggle errors? trigger the action using the `Error` hook.

Want to do something every time a flag is toggled, regardless of the status? `Finally` is probably what you are looking for.

## What Else Does OpenFeature Offer?
Probably lots more than I've covered here. I'm still learning too, but I know conditional and fractional evaluations are possible. For example, you receive `valueA` if the email ends in `@example.com` otherwise `valueB`.

I believe rules can be created like `getColour` where `green` is returned `X%` of the time, `blue` is given `Y%` of the time and so on.

OpenFeature has a concept called `evaluation context` which means you can pass in dynamic data at runtime that can be used by the Provider to evaluate a flag. Imagine traffic on a certain IP range (US-based users) receive one value and and European-based users get a different flag value.

# Where Can I Find Out More?

The [OpenFeature](https://openfeature.dev) website, [GitHub](https://github.com/open-feature) and [#openfeature on CNCF Slack](https://cloud-native.slack.com/archives/C0344AANLA1) are all good starting points.

