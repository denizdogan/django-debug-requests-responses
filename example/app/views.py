from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome!")


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
