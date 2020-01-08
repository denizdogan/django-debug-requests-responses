# Change log

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
