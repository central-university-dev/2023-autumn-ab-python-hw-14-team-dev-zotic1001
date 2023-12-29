import logging.config
from config.settings import app_settings
from fastapi import FastAPI
from .api.auth.auth_app import auth_app

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": app_settings.log_level,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": app_settings.log_level,
    },
}

logging.config.dictConfig(logging_config)


class FastApiBuilder:
    def __init__(self, base_url: str = '', log_disable_level: int | None = None):
        self.base_url = base_url
        self.logging = log_disable_level
        if log_disable_level is not None:
            logging.disable(log_disable_level)

    def create_app(self) -> FastAPI:
        app = FastAPI()
        app.mount("/auth", auth_app)
        return app
