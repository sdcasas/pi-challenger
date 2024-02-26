import os
from starlette.config import Config


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

_config = Config(os.path.join(os.path.dirname(ROOT_DIR), ".env"))

IS_DEBUG: bool = _config("IS_DEBUG", cast=bool, default=False)
DATABASE_URL = _config("DATABASE_URL", cast=str, default=f"sqlite:///db/sqlite.db")

# project
APP_VERSION = "0.0.1"
APP_NAME = "PI Consulting Challenger"
APP_DESCRIPTION = "API with FastAPI"
DOCS_URL: str = "/docs" if IS_DEBUG else None

# admin
ADMIN_ENABLED: bool = _config("ADMIN_ENABLED", cast=bool, default=False)
ADMIN_USERNAME: str = _config("ADMIN_USERNAME", cast=str)
ADMIN_PASSWORD: str = _config("ADMIN_PASSWORD", cast=str)
