import io
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
        "category": "text",
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
        "category": "text",
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
    response = client.post("/upload", data={"category": "text"}, content_type="multipart/form-data")
    assert response.status_code in (302, 400)


@pytest.mark.integration
def test_upload_empty_filename(client):
    """POST /upload com filename vazio — espera redirect com mensagem de erro."""
    data = {
        "file": (io.BytesIO(b"some content"), ""),
        "category": "text",
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
        "category": "text",
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
def test_upload_wrong_extension_for_category(client):
    """POST /upload com extensão incompatível com a categoria — redireciona com erro."""
    data = {
        "file": (io.BytesIO(b"fake binary data"), "archive.bin"),
        "category": "text",
    }
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"suportado" in response.data or b"suporte" in response.data

@pytest.mark.integration
def test_upload_invalid_category(client):
    """POST /upload com categoria inválida — redireciona com erro."""
    data = {
        "file": (io.BytesIO(b"some content"), "test.txt"),
        "category": "invalid_category",
    }
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"inv" in response.data.lower()


# --- Upload por categoria ---

@pytest.mark.integration
def test_upload_pdf_category(client, tmp_path):
    """POST /upload com categoria PDF — aceita arquivo .pdf."""
    content = b"%PDF-1.4 fake pdf content for testing"
    data = {
        "file": (io.BytesIO(content), "document.pdf"),
        "category": "pdf",
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
def test_upload_image_category(client, tmp_path):
    """POST /upload com categoria imagem — aceita arquivo .png."""
    content = b"\x89PNG\r\n\x1a\n fake png content"
    data = {
        "file": (io.BytesIO(content), "photo.png"),
        "category": "image",
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
def test_upload_audio_category(client, tmp_path):
    """POST /upload com categoria áudio — aceita arquivo .mp3."""
    content = b"ID3\x04\x00 fake mp3 content for testing"
    data = {
        "file": (io.BytesIO(content), "song.mp3"),
        "category": "audio",
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


# --- Decompress route ---

@pytest.mark.integration
def test_decompress_route_success(client, tmp_path):
    """POST /decompress com arquivo .huff válido — restaura o arquivo original."""
    from src.huffman.encoder import encode
    from src.huffman.io import write_compressed
    
    original_data = b"hello world for decompress test!"
    bitstring, tree = encode(original_data)
    huff_path = str(tmp_path / "test.huff")
    write_compressed(huff_path, tree, bitstring, "original.txt")
    
    with open(huff_path, 'rb') as f:
        huff_content = f.read()
    
    data = {
        "file": (io.BytesIO(huff_content), "test.huff"),
    }
    response = client.post(
        "/decompress",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200


@pytest.mark.integration
def test_decompress_non_huff_file(client):
    """POST /decompress com arquivo não-.huff — redireciona com erro."""
    data = {
        "file": (io.BytesIO(b"not a huff file"), "test.txt"),
    }
    response = client.post(
        "/decompress",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b".huff" in response.data


@pytest.mark.integration
def test_decompress_no_file(client):
    """POST /decompress sem arquivo — espera redirect com erro."""
    response = client.post("/decompress", data={}, content_type="multipart/form-data")
    assert response.status_code in (302, 400)
