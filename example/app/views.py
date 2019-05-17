from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome!")


def unauthorized(request):
    return HttpResponse("Unauthorized", status=401)
