# Change log

## [Unreleased]

## [4.0.0] - 2026-07-20

With this release, DDRR only supports Python 3.11-3.14 and Django 5.2-6.0.

### Added

- Support for Python 3.12, 3.13, and 3.14
- Support for Django 5.2 and 6.0
- Example route demonstrating safe terminal-control rendering
- Synchronous and asynchronous middleware support

### Changed

- Add Dependabot updates for Python dependencies, pre-commit hooks, and GitHub Actions
- Add local GitHub Actions validation with `act` and `actionlint`
- Validate linting and built distribution artifacts in CI
- Modernize the default request and response output with directional markers, indented headers, and consistent spacing
- Upgrade to pytest 9 and pre-commit 4
- Replace Faker and pytest-mock with standard-library test data and helpers
- Include source doctests in the test suite
- Use Django's built-in request header formatting instead of custom normalization
- Replace Django template rendering with direct request and response formatting

### Fixed

- Continue rendering request logs when the request body has already been consumed #6
- Respect the `ENABLE_REQUESTS` and `ENABLE_RESPONSES` settings
- Prevent logging failures from interrupting request handling
- Prevent duplicate handlers and root propagation from duplicating output
- Emit request and response records at the configured `LEVEL`
- Preserve raw query strings without parsing `request.GET`
- Include every response `Set-Cookie` header in the rendered output
- Restore the example PDF route with a bundled binary document
- Escape terminal controls and indent body output

### Removed

- Django template formatter classes, custom templates, and the `REQUEST_TEMPLATE_NAME`, `REQUEST_TEMPLATE`, `RESPONSE_TEMPLATE_NAME`, and `RESPONSE_TEMPLATE` settings
- `DISABLE_DJANGO_SERVER_LOG`; configure `django.server` through Django's `LOGGING` setting instead
- Optional `lxml` dependency and `xml` extra; XML pretty-printing now uses the Python standard library
- Runtime dependency on attrs
- Support for Python < 3.11
- Support for Django < 5.2

## April 3, 2022 - 3.1.0

- Fix: The request could crash when the log record could not be formatted

## December 1, 2021 - 3.0.0

- Add Python 3.9 support
- Drop Python 3.6 support
- Drop Django < 2.2 support
- Drop `default_app_config`
- Lots of dependency updates
- General clean-up
- Switch CircleCI to GitHub Actions

## October 7, 2020 - 2.0.1

- Fix attrs dependency

## September 23, 2020 - 2.0.0

- Officially support Django 3.x
- Require Python 3.6+ (Django 3.x requires it)
- No changes or bug fixes, that's about it

## January 8, 2020 - 1.3.1

- Fix crash when cleaning HTTP headers #4
- Update pyproject.toml to work with newer Poetry

## December 10, 2019 - 1.3.0

- Fix crash when Content-Type doesn't exist

## September 21, 2019 - 1.2.0

- Add support for streaming responses

## September 18, 2019 - 1.1.1

- (Packaging) Add PyPI classifiers

## September 16, 2019 - 1.1.0

- Handle UnicodeDecodeError if body is not UTF-8 decodable
- Add option to disable runserver's default logging

## September 16, 2019 - 1.0.0

- Replace `quick_setup` with Django settings
- Don't implicitly set up the middleware
- Drop support for Django 1.x and Python 2.x

## May 26, 2019 - 0.3.1

- Use `minidom` as fallback for XML pretty-printing

## May 25, 2019 - 0.3.0

- Add `colors` option
- Add `limit_body` option
- Drop dictConfig-style configuration

## May 18, 2019 - 0.2.0

- Minor change to default output format
- Clean up packaging

## May 18, 2019 - 0.1.1

- Fix package metadata

## May 18, 2019 - 0.1.0

- Initial release

[Unreleased]: https://github.com/denizdogan/django-debug-requests-responses/compare/4.0.0...HEAD
[4.0.0]: https://github.com/denizdogan/django-debug-requests-responses/compare/3.1.0...4.0.0
