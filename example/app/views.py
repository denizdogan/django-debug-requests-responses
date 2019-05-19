from django.http import HttpResponse
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
