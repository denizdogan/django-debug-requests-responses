# Django Debug Requests & Responses (DDRR)

Get more out of your `runserver` development output! Print request and response
headers, body (with pretty-printing), etc.  Highly customizable!

- Log request headers
- Log request body
- Pretty-print JSON request and response bodies
- ...and more!

DDRR can also be used for general logging with some configuration of your own.

## Installation

```
$ pip install ddrr
```

1. Add `ddrr` to your `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = (
        # ...
        "ddrr",
    )
    ```

2. Add the required middleware (nothing will work without this):

    ```python
    MIDDLEWARE = (
        "ddrr.middleware.DebugRequestsResponses",
        # ...
    )
    ```

    It's important that `DebugRequestsResponses` is the first one in the list.

3. Configure the logging of your Django app to use DDRR:

    ```python
    LOGGING = {
        # ...configure as you wish...
    }
    from ddrr import quick_setup
    quick_setup()
    ```

    The `quick_setup` call sets up the default logging configuration which is
    enough for most projects.

4. **Done!**

## Customization

### Change output formats

TODO

## How it works

The middleware `ddrr.middleware.DebugRequestsResponses` sends the entire
request object as the message to `ddrr-request-logger`.  This logger has been
configured to use `ddrr.formatters.DefaultRequestFormatter` which internally
uses Django's built-in template engine to format the request into human-readable
form. By default, this is shown in your console output, but you can easily
configure it to log it to a file, ElasticSearch, or anything else.

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
