# Django Debug Requests & Responses (DDRR)

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

```
$ pip install ddrr
```

```python
# in settings.py
INSTALLED_APPS = (
    # ...
    "ddrr",
)

import ddrr
ddrr.quick_setup()
```

**Done!** When you run `runserver`, you'll now get the entire HTTP requests and
responses, including headers and bodies.

If you don't like the default output format, read on...

### Customization

`ddrr.quick_setup` accepts the following optional arguments:

- `enable_requests` - (default: True) Enable request logging.
- `enable_responses` - (default: True) Enable response logging.
- `level` - (default: DEBUG) The level of the log messages.
- `pretty` - (default: False) Enable pretty-printing of bodies.
- `request_template` - (default: None) Request template string
- `request_template_name` - (default: None) Request template name
- `response_template` - (default: None) Response template string
- `response_template_name` - (default: None) Response template name
- `limit_body` - (default: None) Limit request and response body length
- `colors` - (default: True) Enable color support if terminal supports it

### Change output formats

You can pass `request_template` or `request_template_name` to `quick_setup` to
define a different output format for request logs. The same goes for responses,
use `response_template` or `response_template_name`.

The templates are normal Django templates which are passed the necessary
template context with access to pretty much anything you could be interested in.

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
ddrr.quick_setup(
    request_template="{{ ddrr.method }} {{ ddrr.path }}\n"
                     "{{ ddrr.body }}",
    response_template="{{ ddrr.status_code }} {{ ddrr.reason_phrase }}\n"
                      "{{ ddrr.content }}",
)
```

### How it works internally

The middleware `ddrr.middleware.DebugRequestsResponses` sends the entire
request object as the message to `ddrr-request-logger`.  This logger has been
configured to use `ddrr.formatters.DjangoTemplateRequestFormatter` which
internally uses Django's built-in template engine to format the request into
human-readable form. By default, this is shown in your console output, but you
can easily configure it to log it to a file, ElasticSearch, or anything else.

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
