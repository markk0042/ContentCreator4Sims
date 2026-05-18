from .main import create_app
from waitress import serve

app = create_app()
print("ContentCreator4Sims worker at http://127.0.0.1:8000")
serve(app, host="127.0.0.1", port=8000, threads=4)
