import os
from flask import Blueprint, request, redirect, url_for, render_template, send_file, abort, current_app

from src.huffman.encoder import encode
from src.huffman.io import write_compressed
from src.huffman.decompressor import decompress_file
from src.huffman.rle import rle_encode

bp = Blueprint("main", __name__)

CATEGORY_EXTENSIONS = {
    "text":  {".txt", ".md", ".csv", ".log", ".py", ".json", ".xml", ".html"},
    "pdf":   {".pdf"},
    "image": {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".svg"},
    "audio": {".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma"},
}


@bp.route("/", methods=["GET"])
def index():
    """Página inicial com o formulário de upload."""
    error = request.args.get("error")
    return render_template("index.html", error=error)


@bp.route("/upload", methods=["POST"])
def upload():
    """
    Recebe o arquivo via multipart/form-data, comprime com Huffman
    e salva o .huff na pasta de upload.
    Redireciona para /result com estatísticas de compressão.
    """
    if "file" not in request.files:
        return redirect(url_for("main.index", error="Nenhum arquivo foi enviado."))

    file = request.files["file"]

    if file.filename == "":
        return redirect(url_for("main.index", error="Nome de arquivo vazio."))

    category = request.form.get("category", "text")

    if category not in CATEGORY_EXTENSIONS:
        return redirect(url_for("main.index", error="Categoria inválida."))

    _, ext = os.path.splitext(file.filename.lower())
    allowed = CATEGORY_EXTENSIONS[category]
    if ext and ext not in allowed:
        return redirect(
            url_for("main.index", error=f"Tipo de arquivo '{ext}' não suportado para a categoria '{category}'.")
        )

    data = file.read()

    if len(data) == 0:
        return redirect(url_for("main.index", error="O arquivo está vazio."))

    # Pipeline: RLE → Huffman
    rle_data = rle_encode(data)
    bitstring, tree = encode(rle_data)

    original_filename = file.filename if file.filename else "output.bin"
    base_name = os.path.splitext(original_filename)[0]
    output_filename = base_name + ".huff"
    output_path = os.path.join(current_app.config["UPLOAD_FOLDER"], output_filename)

    write_compressed(output_path, tree, bitstring, original_filename)

    # Estatísticas reais
    original_size = len(data)
    compressed_size = os.path.getsize(output_path)
    ratio = round((1 - compressed_size / original_size) * 100, 2) if original_size > 0 else 0.0

    return redirect(
        url_for(
            "main.result",
            filename=output_filename,
            original_size=original_size,
            compressed_size=compressed_size,
            ratio=ratio,
            mode="compress",
        )
    )


@bp.route("/decompress", methods=["POST"])
def decompress():
    """
    Recebe um arquivo .huff, descompacta e serve o arquivo original restaurado.
    """
    if "file" not in request.files:
        return redirect(url_for("main.index", error="Nenhum arquivo foi enviado."))

    file = request.files["file"]

    if file.filename == "":
        return redirect(url_for("main.index", error="Nome de arquivo vazio."))

    _, ext = os.path.splitext(file.filename.lower())
    if ext != ".huff":
        return redirect(url_for("main.index", error="Para descompactar, envie um arquivo .huff."))

    huff_filename = file.filename if file.filename else "upload.huff"
    huff_path = os.path.join(current_app.config["UPLOAD_FOLDER"], huff_filename)
    file.save(huff_path)

    try:
        restored_path, stats = decompress_file(huff_path, current_app.config["UPLOAD_FOLDER"])
    except (ValueError, Exception) as e:
        return redirect(url_for("main.index", error=f"Erro ao descompactar: {str(e)}"))

    return redirect(
        url_for(
            "main.result",
            filename=stats["original_filename"],
            original_size=stats["restored_size"],
            compressed_size=stats["compressed_size"],
            ratio=round((1 - stats["compressed_size"] / stats["restored_size"]) * 100, 2) if stats["restored_size"] > 0 else 0,
            mode="decompress",
        )
    )


@bp.route("/result", methods=["GET"])
def result():
    """Página de resultado com as estatísticas da compressão/descompactação."""
    filename = request.args.get("filename", "")
    original_size = request.args.get("original_size", 0, type=int)
    compressed_size = request.args.get("compressed_size", 0, type=int)
    ratio = request.args.get("ratio", 0.0, type=float)
    mode = request.args.get("mode", "compress")

    return render_template(
        "result.html",
        filename=filename,
        original_size=original_size,
        compressed_size=compressed_size,
        ratio=ratio,
        mode=mode,
    )


@bp.route("/download/<filename>", methods=["GET"])
def download(filename: str):
    """
    Serve o arquivo comprimido ou restaurado para download.
    Retorna 404 se o arquivo não existir.
    """
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, filename)

    if not os.path.isfile(file_path):
        abort(404)

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream",
    )
