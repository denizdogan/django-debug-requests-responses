from example.app.views import pdf_file
from example.app.views import terminal_controls


def test_terminal_controls_example(rf):
    response = terminal_controls(rf.get("/terminal_controls"))

    assert response.status_code == 200
    assert response["Content-Type"] == "text/plain"
    assert response.content.decode() == (
        "normal line\n→ forged response\x1b[31m red text\x1b[0m\n"
    )


def test_pdf_example(rf):
    response = pdf_file(rf.get("/pdf_file"))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
    assert response.content.startswith(b"%PDF-")
    assert b"\xe2\xe3\xcf\xd3" in response.content
    assert response.content.rstrip().endswith(b"%%EOF")
