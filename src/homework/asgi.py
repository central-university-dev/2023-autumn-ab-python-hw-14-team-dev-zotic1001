import logging.config

from faker import Faker
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User, Word, Category
from config.settings import app_settings
from .contracts import Message

fake = Faker()

app = FastAPI()

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

engine = create_engine(app_settings.db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/", response_model=Message)
async def root() -> Message:
    return Message(message="Hello that", code=1)
