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
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    if config:
        app.config.update(config)

    from src.web.routes import bp
    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
