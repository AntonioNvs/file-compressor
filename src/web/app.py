import os
from flask import Flask


def create_app(config: dict | None = None) -> Flask:
    """
    Application factory do Flask.
    Cria e configura a instância da aplicação.
    """
    app = Flask(__name__, template_folder="templates")

    upload_folder = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = upload_folder
    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024  # 32 MB
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    if config:
        app.config.update(config)

    from src.web.routes import bp
    app.register_blueprint(bp)

    return app


# Para rodar a aplicação, use a partir da raiz do projeto:
#   python run.py
# ou:
#   python -m src.web.app
