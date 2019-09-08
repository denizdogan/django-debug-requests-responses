from app.views import index
from app.views import ugly_json
from app.views import ugly_xml
from app.views import unauthorized
from django.urls import path

urlpatterns = [
    path("", index),
    path("401", unauthorized),
    path("ugly_xml", ugly_xml, name="ugly_xml"),
    path("ugly_json", ugly_json, name="ugly_json"),
]
