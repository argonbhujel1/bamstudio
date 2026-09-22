"""Vercel serverless entry (api/). Strips /api prefix so Flask routes match."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app as flask_app  # noqa: E402


class _PathFix:
    """Map /api and /api/... → / and /... for Flask."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "") or "/"
        # Vercel may pass /api, /api/, or /api/foo
        if path == "/api" or path == "/api/":
            environ["PATH_INFO"] = "/"
        elif path.startswith("/api/"):
            environ["PATH_INFO"] = path[4:] or "/"
        return self.app(environ, start_response)


app = _PathFix(flask_app)
application = app
handler = app
