from pathlib import Path

from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "app/index.html")


def unauthorized(request):
    return HttpResponse("Unauthorized", status=401)


def ugly_xml(request):
    return HttpResponse(
        """
        <message>
        <from>   John Doe</from>
            <to>Jane   </to><body>
        God I wish we had a pretty printer...
    </body></message>
    """,
        content_type="text/xml",
    )


def ugly_json(request):
    return HttpResponse(
        """
        {
         "message": {
                    "from": "John Doe",
            "to": "Jane",
                    "body": "God I wish we had a pretty printer..."
                }
        }
        """,
        content_type="application/json",
    )


def pdf_file(request):
    content = (Path(__file__).resolve().parent / "pdf.pdf").read_bytes()
    return HttpResponse(content, content_type="application/pdf")


def stream(request):
    def hello():
        yield "Hello, "
        yield "World"

    return StreamingHttpResponse(hello())
