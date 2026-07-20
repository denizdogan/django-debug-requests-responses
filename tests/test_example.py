from example.app.views import pdf_file


def test_pdf_example(rf):
    response = pdf_file(rf.get("/pdf_file"))

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"
    assert response.content.startswith(b"%PDF-")
    assert b"\xe2\xe3\xcf\xd3" in response.content
    assert response.content.rstrip().endswith(b"%%EOF")
