# Django Debug Requests & Responses (DDRR)

[![CircleCI](https://circleci.com/gh/denizdogan/django-debug-requests-responses/tree/master.svg?style=svg)](https://circleci.com/gh/denizdogan/django-debug-requests-responses/tree/master)

Get more out of your `runserver` development output! Print request and response
headers, body (with pretty-printing), etc.  Highly customizable!

- Full request headers
- The entire request body
- Pretty-printing optional
- Colored output
- Super easy setup
- No extra dependencies

DDRR can also be used for general logging with some configuration of your own.

## Installation

1. ```
   $ pip install ddrr
   ```

2. Add `"ddrr"` to `INSTALLED_APPS`

3. Insert `"ddrr.middleware.DebugRequestsResponses"` first in `MIDDLEWARE`

**Done!** When you run `runserver`, you'll now get the entire HTTP requests and
responses, including headers and bodies.

If you don't like the default output format, read on...

## Customization

```python
DDRR = {
    "ENABLE_REQUESTS": True,  # enable request logging
    "ENABLE_RESPONSES": True,  # enable response logging
    "LEVEL": "DEBUG",  # ddrr log level
    "PRETTY_PRINT": False,  # pretty-print JSON and XML
    "REQUEST_TEMPLATE_NAME": "ddrr/default-request.html",  # request log template name
    "REQUEST_TEMPLATE": None,  # request log template string (overrides template name)
    "RESPONSE_TEMPLATE_NAME": "ddrr/default-response.html",  # response log template name
    "RESPONSE_TEMPLATE": None,  # response log template string (overrides template name)
    "REQUEST_HANDLER": logging.StreamHandler(),  # request log handler
    "RESPONSE_HANDLER": logging.StreamHandler(),  # response log handler
    "ENABLE_COLORS": True,  # enable colors if terminal supports it
    "LIMIT_BODY": None,  # limit request/response body output to X chars
    "DISABLE_DJANGO_SERVER_LOG": False,  # disable default django server log
}
```

### Template contexts

If you want to customize request or response templates, you can use the following values:

- **Request template context:**
  - `ddrr.body` - request body
  - `ddrr.content_type` - request content type
  - `ddrr.formatter` - the formatter
  - `ddrr.headers` - mapping of header fields and values
  - `ddrr.method` - request method
  - `ddrr.path` - request path
  - `ddrr.query_params` - query parameters
  - `ddrr.query_string` - query string
  - `ddrr.record` - the actual log record object
  - `ddrr.request` - the actual request object
- **Response template context:**
  - `ddrr.content` - response content
  - `ddrr.content_type` - response content type
  - `ddrr.formatter` - the formatter
  - `ddrr.headers` - mapping of header fields and values
  - `ddrr.reason_phrase` - response reason phrase
  - `ddrr.record` - the actual log record object
  - `ddrr.response` - the actual response object
  - `ddrr.status_code` - response status code

For example, this will log the method, path and body of each request, as well
as the status code, reason phrase and content of each response:

```python
DDRR = {
    "REQUEST_TEMPLATE": "{{ ddrr.method }} {{ ddrr.path }}\n"
                        "{{ ddrr.body }}",
    "RESPONSE_TEMPLATE": "{{ ddrr.status_code }} {{ ddrr.reason_phrase }}\n"
                         "{{ ddrr.content }}",
}
```

### Pretty-printing

By default, pretty-printing is disabled.  Set `DDRR["PRETTY_PRINT"]` to `True`
to enable it.

Pretty-printing of JSON requires no external dependency.

Pretty-printing of XML uses `minidom` by default and doesn't require any extra
dependency. If you want to use `lxml` instead, which is slightly better at
pretty-printing XML, you can install that using `pip install ddrr[xml]`.

## How it works internally

The middleware `ddrr.middleware.DebugRequestsResponses` sends the entire
request object as the message to `ddrr-request-logger`.  This logger has been
configured to use `ddrr.formatters.DjangoTemplateRequestFormatter` which
internally uses Django's built-in template engine to format the request into
human-readable form. By default, this is shown in your console output, but you
can easily configure it to log it to a file, Logstash, or anything else.

## Similar projects

- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io)

## Development and contributions

PR's are always welcome!

For hacking on DDRR, make sure you are familiar with:

- [Black](https://github.com/ambv/black)
- [Flake8](http://flake8.pycqa.org/)
- [Poetry](https://poetry.eustace.io/)
- [pre-commit](https://github.com/pre-commit/pre-commit)
- [pytest](https://docs.pytest.org)

Install dependencies and set up the pre-commit hooks.

```
$ poetry install
$ pre-commit install
```

The pre-commit hooks will, among other things, run Flake8 on the code base and
Black to make sure the code style is consistent across all files.  Check out
[`.pre-commit-config.yaml`](.pre-commit-config.yaml) for details.
