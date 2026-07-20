# Django Debug Requests & Responses (DDRR)

Get more out of your `runserver` development output! Print request and response
headers, body (with pretty-printing), etc.  Highly customizable! Supports
Django 5.2-6.0 with Python 3.11-3.14.

> **Warning:** DDRR is intended only for trusted development environments. It
> logs headers—including authorization and cookie headers—and bodies without
> redaction. Do not enable it where this data or the resulting logs may be
> exposed to untrusted users.

- Full request headers
- Request and response bodies when available
- Pretty-printing optional
- Colored output
- Super easy setup
- No extra dependencies

DDRR can also be used for general logging with some configuration of your own.

## Installation

1. ```console
   $ pip install ddrr
   ```

2. Add `"ddrr"` to `INSTALLED_APPS`

3. Insert `"ddrr.middleware.DebugRequestsResponses"` first in `MIDDLEWARE`

**Done!** When you run `runserver`, you'll see requests and responses, including
headers and available bodies.

To adjust DDRR's logging behavior, read on...

## Customization

```python
import logging
DDRR = {
    "ENABLE_REQUESTS": True,  # enable request logging
    "ENABLE_RESPONSES": True,  # enable response logging
    "LEVEL": "DEBUG",  # ddrr log level
    "PRETTY_PRINT": False,  # pretty-print JSON and XML
    "REQUEST_HANDLER": logging.StreamHandler(),  # request log handler
    "RESPONSE_HANDLER": logging.StreamHandler(),  # response log handler
    "ENABLE_COLORS": True,  # enable colors if terminal supports it
    "LIMIT_BODY": None,  # limit request/response body output to X chars
    "DISABLE_DJANGO_SERVER_LOG": False,  # disable default django server log
}
```

### Output safety

DDRR renders terminal control characters as visible escape sequences. Newlines
inside single-line fields such as paths and headers are escaped, while body
newlines are preserved and every body line is indented so it cannot resemble a
separate request or response log entry.

### Pretty-printing

By default, pretty-printing is disabled.  Set `DDRR["PRETTY_PRINT"]` to `True`
to enable it.

Pretty-printing of JSON and XML uses the Python standard library and requires
no external dependencies.

## How it works internally

The middleware `ddrr.middleware.DebugRequestsResponses` sends request and
response objects to separate loggers. DDRR's formatters turn them into fixed,
human-readable output. By default, this is shown in your console, but you can
configure the handlers to send it elsewhere.

## Similar projects

- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io)

## Development and contributions

PRs are always welcome!

For hacking on DDRR, make sure you are familiar with:

- [mise](https://mise.jdx.dev/)
- [act](https://nektosact.com/)
- [actionlint](https://github.com/rhysd/actionlint)
- [Ruff](https://docs.astral.sh/ruff/)
- [ty](https://docs.astral.sh/ty/)
- [uv](https://docs.astral.sh/uv/)
- [pre-commit](https://github.com/pre-commit/pre-commit)
- [pytest](https://docs.pytest.org)

### Set up environment

Install the locked tool versions using mise, sync the project environment using
uv, then install the pre-commit hooks. mise automatically creates and activates
the project's `.venv` when entering the repository.

```console
$ mise install
$ mise exec -- uv sync
$ mise exec -- uv run pre-commit install
```

> The pre-commit hooks will, among other things, use Ruff to lint and format
> Python code and ty to check types. The full pre-commit configuration exists
> in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

### GitHub Actions

With Docker running, run the GitHub Actions workflow locally using act:

```console
$ mise run act
```

Pass additional act options after `--`, for example `mise run act -- --list`.
Workflow files are also checked with actionlint by pre-commit.

### Type checking

Run ty using the current Python interpreter and project environment:

```console
$ mise exec -- ty check
```

### Running tests

Run tests using the current Python interpreter and currently installed Django
version.

```console
$ mise exec -- uv run pytest
```

Run tests with every supported Python and Django combination:

```console
$ mise exec -- uv run tox
```

### Running GitHub Actions locally

Use [act](https://github.com/nektos/act).

```console
$ act
```

If you are running macOS, you may need to use:

```console
$ act --container-architecture linux/amd64
```
