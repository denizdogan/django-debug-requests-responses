from app.views import (
    index,
    pdf_file,
    stream,
    terminal_controls,
    ugly_json,
    ugly_xml,
    unauthorized,
)
from django.urls import path

urlpatterns = [
    path("", index),
    path("401", unauthorized),
    path("pdf_file", pdf_file, name="pdf_file"),
    path("stream", stream, name="stream"),
    path("terminal_controls", terminal_controls, name="terminal_controls"),
    path("ugly_json", ugly_json, name="ugly_json"),
    path("ugly_xml", ugly_xml, name="ugly_xml"),
]
