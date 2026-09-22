import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def _normalize_database_url(url: str) -> str:
    if not url or not str(url).strip():
        return "sqlite:///bam_studio.db"

    url = str(url).strip().strip('"').strip("'")

    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        bad = {"host", "hostname", "your-host", "xxx", "example.com", "localhost.neon.tech"}
        if hostname in bad or not hostname:
            print(f"[config] Invalid DATABASE_URL host={hostname!r} — falling back to SQLite")
            return "sqlite:///bam_studio.db"
        if parsed.scheme.startswith("postgresql") and "sslmode=" not in url:
            url += ("&" if "?" in url else "?") + "sslmode=require"
    except Exception as e:
        print(f"[config] DATABASE_URL error: {e}")
        return "sqlite:///bam_studio.db"

    return url


_db_url = _normalize_database_url(
    os.environ.get("DATABASE_URL")
    or os.environ.get("POSTGRES_URL")
    or os.environ.get("POSTGRES_PRISMA_URL")
    or "sqlite:///bam_studio.db"
)


def _engine_options():
    if not _db_url.startswith("postgresql"):
        return {}
    opts = {
        "pool_pre_ping": True,
        "connect_args": {"connect_timeout": 15, "sslmode": "require"},
    }
    try:
        from sqlalchemy.pool import NullPool
        opts["poolclass"] = NullPool
    except Exception:
        pass
    return opts


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-in-production-bam-studio-2026"
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = _engine_options()

    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET", "")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg", "woff", "woff2", "ttf", "otf"}

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("VERCEL") == "1"
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = False
    WTF_CSRF_TIME_LIMIT = None
    SESSION_REFRESH_EACH_REQUEST = True
