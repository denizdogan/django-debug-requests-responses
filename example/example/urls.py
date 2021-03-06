from app.views import index
from app.views import pdf_file
from app.views import stream
from app.views import ugly_json
from app.views import ugly_xml
from app.views import unauthorized
from django.urls import path

urlpatterns = [
    path("", index),
    path("401", unauthorized),
    path("pdf_file", pdf_file, name="pdf_file"),
    path("stream", stream, name="stream"),
    path("ugly_json", ugly_json, name="ugly_json"),
    path("ugly_xml", ugly_xml, name="ugly_xml"),
]
