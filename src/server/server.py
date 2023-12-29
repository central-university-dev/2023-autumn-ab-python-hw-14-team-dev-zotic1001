import logging.config

from faker import Faker
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import app_settings
from .contracts import Token, AuthAttributes
from db.users import UsersRepo


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
SessionLocal = sessionmaker(autoflush=False, bind=engine)


@app.post("/auth", response_model=Token)
def authorization(auth_attributes: AuthAttributes) -> Token:
    with SessionLocal() as session:
        users_table = UsersRepo(session)
        return users_table.login_user(auth_attributes)


@app.post("/register", response_model=Token)
def register(auth_attributes: AuthAttributes) -> Token:
    with SessionLocal() as session:
        users_table = UsersRepo(session)
        token = users_table.add_user(auth_attributes)
        session.commit()
    return token
