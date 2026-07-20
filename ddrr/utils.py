import json
import re
from collections import OrderedDict
from xml.etree import ElementTree


def pretty_print_xml(content):
    """
    Pretty-print an XML string and return it.

    >>> pretty_print_xml('')
    ''
    >>> pretty_print_xml('<p></u>')
    '<p></u>'
    >>> pretty_print_xml('<p><div><b>hel</b>lo!</div></p>')
    '<p>\\n  <div>\\n    <b>hel</b>lo!</div>\\n</p>'

    :param content: XML string
    :return: Pretty-printed XML string
    """
    try:
        root = ElementTree.fromstring(content)
        ElementTree.indent(root, space="  ")
        return ElementTree.tostring(root, encoding="unicode")
    except ElementTree.ParseError:
        return content


def pretty_print_json(content):
    """
    Pretty-print a JSON string and return it.

    >>> pretty_print_json('')
    ''
    >>> pretty_print_json('foobar')
    'foobar'
    >>> pretty_print_json('{"foo":"bar"}')
    '{\\n  "foo": "bar"\\n}'
    >>> pretty_print_json('   {"foo"  : "bar"  }')
    '{\\n  "foo": "bar"\\n}'

    :param content: JSON string
    :return: Pretty-printed JSON string
    """
    try:
        data = json.loads(content)
        return json.dumps(data, indent=2)
    except json.decoder.JSONDecodeError:
        return content


PRETTY_PRINTERS = OrderedDict(
    (
        (r"/json", pretty_print_json),
        (r"/xml", pretty_print_xml),
    ),
)


def pretty_print(content, content_type):
    for regex, handler in PRETTY_PRINTERS.items():
        if re.search(regex, content_type):
            return handler(content)
    return content
