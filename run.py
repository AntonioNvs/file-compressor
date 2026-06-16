"""
Ponto de entrada para rodar a aplicação Flask a partir da raiz do projeto.

Uso:
    python run.py
"""
from src.web.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
