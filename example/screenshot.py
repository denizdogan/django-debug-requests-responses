import os
import sys
from io import BytesIO

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

application = get_wsgi_application()
environ = {
    "HTTP_HOST": "localhost",
    "PATH_INFO": "/ugly_json",
    "QUERY_STRING": "",
    "REQUEST_METHOD": "GET",
    "SCRIPT_NAME": "",
    "SERVER_NAME": "localhost",
    "SERVER_PORT": "80",
    "SERVER_PROTOCOL": "HTTP/1.1",
    "wsgi.errors": sys.stderr,
    "wsgi.input": BytesIO(),
    "wsgi.multiprocess": False,
    "wsgi.multithread": False,
    "wsgi.run_once": False,
    "wsgi.url_scheme": "http",
    "wsgi.version": (1, 0),
}

response = application(environ, lambda status, headers: None)
try:
    b"".join(response)
finally:
    response.close()
