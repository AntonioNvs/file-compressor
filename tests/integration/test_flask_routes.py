import io
import os
import pytest
from src.web.app import create_app


@pytest.fixture
def client(tmp_path):
    """Cria um test client Flask com pasta de upload temporária."""
    app = create_app(
        {
            "TESTING": True,
            "UPLOAD_FOLDER": str(tmp_path),
        }
    )
    with app.test_client() as c:
        yield c


@pytest.mark.integration
def test_upload_route_success(client, tmp_path):
    """POST /upload com arquivo de texto válido — verifica redirect e arquivo .huff gerado."""
    content = b"the quick brown fox jumps over the lazy dog"
    data = {
        "file": (io.BytesIO(content), "sample.txt"),
    }
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    huff_files = list(tmp_path.glob("*.huff"))
    assert len(huff_files) == 1


@pytest.mark.integration
def test_download_route_success(client, tmp_path):
    """GET /download/<filename> — upload primeiro, depois verifica o download."""
    content = b"hello huffman compression world"
    data = {
        "file": (io.BytesIO(content), "testfile.txt"),
    }
    client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
    )

    huff_files = list(tmp_path.glob("*.huff"))
    assert len(huff_files) == 1, "Arquivo .huff não foi criado pelo upload"

    filename = huff_files[0].name
    response = client.get(f"/download/{filename}")
    assert response.status_code == 200
    assert response.headers.get("Content-Disposition", "").startswith("attachment")
    assert len(response.data) > 0


@pytest.mark.integration
def test_upload_no_file(client):
    """POST /upload sem arquivo — espera redirect com mensagem de erro."""
    response = client.post("/upload", data={}, content_type="multipart/form-data")
    assert response.status_code in (302, 400)


@pytest.mark.integration
def test_upload_empty_filename(client):
    """POST /upload com filename vazio — espera redirect com mensagem de erro."""
    data = {
        "file": (io.BytesIO(b"some content"), ""),
    }
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code in (302, 400)


@pytest.mark.integration
def test_upload_empty_file(client):
    """POST /upload com arquivo de 0 bytes — espera redirect de erro."""
    data = {
        "file": (io.BytesIO(b""), "empty.txt"),
    }
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code in (302, 400)


@pytest.mark.integration
def test_upload_binary_file(client):
    """POST /upload com arquivo binário não-texto — espera tratamento de erro."""
    binary_content = bytes(range(256))
    data = {
        "file": (io.BytesIO(binary_content), "binary.bin"),
    }
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code in (302, 400)


@pytest.mark.integration
def test_download_nonexistent_file_returns_404(client):
    """GET /download/<inexistente> retorna 404."""
    response = client.get("/download/arquivo_que_nao_existe.huff")
    assert response.status_code == 404


@pytest.mark.integration
def test_upload_unsupported_extension(client):
    """POST /upload com extensão não suportada (.bin) — redireciona com erro."""
    data = {
        "file": (io.BytesIO(b"fake binary data"), "archive.bin"),
    }
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"suportado" in response.data or b"suporte" in response.data or response.status_code in (302, 400)
