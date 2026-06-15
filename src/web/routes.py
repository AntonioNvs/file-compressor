import os
from flask import Blueprint, request, redirect, url_for, render_template, send_file, abort, current_app

from src.huffman.encoder import encode, get_stats
from src.huffman.io import write_compressed

bp = Blueprint("main", __name__)


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

    ALLOWED_EXTENSIONS = {".txt", ".md", ".csv", ".log", ".py", ".json", ".xml", ".html"}
    _, ext = os.path.splitext(file.filename.lower())
    if ext and ext not in ALLOWED_EXTENSIONS:
        return redirect(
            url_for("main.index", error=f"Tipo de arquivo não suportado: '{ext}'. Envie um arquivo de texto.")
        )

    try:
        text = file.read().decode("utf-8")
    except (UnicodeDecodeError, Exception):
        return redirect(
            url_for("main.index", error="Arquivo inválido: apenas arquivos de texto UTF-8 são suportados.")
        )

    if len(text) == 0:
        return redirect(url_for("main.index", error="O arquivo está vazio."))

    bitstring, tree = encode(text)
    stats = get_stats(text)

    base_name = os.path.splitext(file.filename)[0] if file.filename else "output"
    output_filename = base_name + ".huff"
    output_path = os.path.join(current_app.config["UPLOAD_FOLDER"], output_filename)

    write_compressed(output_path, tree, bitstring)

    return redirect(
        url_for(
            "main.result",
            filename=output_filename,
            original_size=stats["original_size"],
            compressed_size=stats["compressed_size"],
            ratio=round(stats["ratio"], 2),
        )
    )


@bp.route("/result", methods=["GET"])
def result():
    """Página de resultado com as estatísticas da compressão."""
    filename = request.args.get("filename", "")
    original_size = request.args.get("original_size", 0, type=int)
    compressed_size = request.args.get("compressed_size", 0, type=int)
    ratio = request.args.get("ratio", 0.0, type=float)

    return render_template(
        "result.html",
        filename=filename,
        original_size=original_size,
        compressed_size=compressed_size,
        ratio=ratio,
    )


@bp.route("/download/<filename>", methods=["GET"])
def download(filename: str):
    """
    Serve o arquivo comprimido para download.
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
