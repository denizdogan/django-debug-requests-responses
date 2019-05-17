import logging
import re


class GenericAttributeFilter(logging.Filter):
    def __init__(self, name="", field="", regex=""):
        """
        Filter requests based on one of their attributes.

        >>> GenericAttributeFilter(field='foo', regex='aaa').field
        'foo'
        >>> GenericAttributeFilter(field='foo', regex='aaa').regex
        re.compile('aaa')

        :param name: Filter name
        :param field: Field name
        :param regex: Regular expression
        """
        self.field = field
        self._regex = regex
        self._compiled = None
        super().__init__(name)

    @property
    def regex(self):
        if not self._compiled:
            self._compiled = re.compile(self._regex)
        return self._compiled

    def filter(self, record):
        value = getattr(record.msg, self.field, None)
        if value is None:
            return True  # allow non-matching ones
        return self.regex.match(value)


class StatusCodeFilter(GenericAttributeFilter):
    def __init__(self, name="", status_codes=""):
        """
        Filter responses based on their status codes.

        >>> StatusCodeFilter().status_codes
        []
        >>> StatusCodeFilter(status_codes="404").status_codes
        [404]
        >>> StatusCodeFilter(status_codes="401,404").status_codes
        [401, 404]

        :param name: Filter name
        :param status_codes: Disallowed status codes as comma-separated string
        """
        self.status_codes = (
            len(status_codes) and list(map(int, status_codes.split(","))) or []
        )
        super().__init__(name)

    def filter(self, record):
        return not (
            hasattr(record.msg, "status_code")
            and record.msg.status_code in self.status_codes
        )


class PathFilter(GenericAttributeFilter):
    """
    Example configuration:
    {
        "()": "ddrr.filters.PathFilter",
        "regex": "\\/favicon.*",
    }
    """

    def __init__(self, **kwargs):
        super().__init__(field="path", **kwargs)
