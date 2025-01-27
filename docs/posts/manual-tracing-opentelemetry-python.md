---

title: 'Manual OpenTelemetry Tracing in Python: Beginners Guide'
categories:
- opentelemetry
- python
- instrumentation
- tutorial
date:
  created: 2024-04-13
---

In this post, you will take your first steps to manually instrumenting a Python application using OpenTelemetry.

<!-- more -->

I recently posted a video (see below) and this is the text version for those who prefer to read instead.

If you got here and want to watch, just click the image below.

[![Manually Instrument a Python application with OpenTelemetry: YouTube](https://img.youtube.com/vi/iVQmhMLEkS0/0.jpg)](https://www.youtube.com/watch?v=iVQmhMLEkS0)

## Start with the Basics

Start by writing a very simple function called `add` which takes two parameters: `first` and `second`. The function just adds these two numbers and returns them to you.

Give yourself a way to run it too (with the `__name__ == "__main__"` block).

Save this code as `app.py`.

```python
def add(first, second):
    return first + second

if __name__ == "__main__":
    return_value = add(11, 3)
    print(f"The return value is: {return_value}")
```

Run the code with `python app.py` and you should see:

```sh
The return value is: 14
```

## OpenTelemetry Requirements

We want to track how long it takes to add those two numbers, so start adding the OpenTelemetry code now.

Create a file called `requirements.txt` and add this content (note: Go to PyPi to get the latest version numbers).

```
opentelemetry-sdk == 1.24.0
opentelemetry-api == 1.24.0
```

Install these dependencies now: `pip install -r requirements.txt`

## The OpenTelemetry Boilerplate

Copy the boilerplate code from [this page](https://opentelemetry.io/docs/languages/python/instrumentation/#traces) and paste it above your existing code.

Your `app.py` should now look like this:

```
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

def add(first, second):
    return first + second

if __name__ == "__main__":
    return_value = add(11, 3)
    print(f"The return value is: {return_value}")
```

This code sets up OpenTelemetry, ready to trace and uses the `ConsoleSpanExporter` to tell OpenTelemetry to output the spans to, unsurprisingly, the console window.

If you re-run this code now, nothing new will happen. We need one more step.

## Tell OpenTelemetry to Create the Span

A span is a single unit of work. For example, a span may track a single function call (as in our example) or you may decided to split a longer function into multiple spans. That's up to you.

There are two ways to create a span. Using a `with` block or using a decorator. We will use a decorator.

Above this line: `def add(first, second):` add the following:

```python
@tracer.start_as_current_span("add")
```

This tells the OpenTelemetry tracer (defined on line 16) that when the `add` function is executed, OpenTelemetry should create a span (which starts and ends when the function does) and the span should also be called `add`.

Your code should now look like this:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

@tracer.start_as_current_span("add")
def add(first, second):
    return first + second

if __name__ == "__main__":
    return_value = add(11, 3)
    print(f"The return value is: {return_value}")
```

The output should look similar to this:

```
The return value is: 14
{
    "name": "add",
    "context": {
        "trace_id": "0xf9030d21e7e46e03dc17605e38976d0d",
        "span_id": "0x089a2d951c598f4e",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2024-04-13T06:43:07.534014Z",
    "end_time": "2024-04-13T06:43:07.534023Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {},
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.24.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
```

🎉 Congratulations! 🎉 That JSON blob is your OpenTelemetry span.

Stay tuned (or [subscribe to my YouTube channel](https://www.youtube.com/@agardnerit?sub_confirmation=1)) for the next tutorial where I explain each field and enrich the span with events, metadata and a correct status code. See you then!