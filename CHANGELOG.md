# Change log

## [Unreleased]

With this release, DDRR only supports Python 3.8-3.11 and Django 3.2-4.1.

### Added

- Support for Python 3.10 and 3.11

### Removed

- Support for Python < 3.8
- Support for Django < 3.2

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

- [unreleased]: https://github.com/denizdogan/django-debug-requests-responses/compare/3.1.0...HEAD
