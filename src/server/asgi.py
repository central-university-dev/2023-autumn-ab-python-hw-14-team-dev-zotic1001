import logging.config
from typing import Annotated

from faker import Faker
from fastapi import FastAPI, HTTPException, status, Header
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import app_settings
from db.words_repo import WordsRepo
from .contracts import Token, AuthAttributes, WordContract
from db.users import UsersRepo
import jwt

from ..word import wordClient

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
        session.commit()
        return users_table.add_user(auth_attributes)


def login(token: str):
    try:
        user_data = jwt.decode(
            token, app_settings.secret_key, "HS256"
        )
        return user_data
    except jwt.exceptions.InvalidTokenError:
        return None


@app.get("/word", response_model=WordContract)
def get_word(header: Annotated[str | None, Header()]):
    user_data = login(header)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
            headers={"WWW-Authenticate": "Basic"},
        )
    resp = wordClient.get_word_and_translate()
    with SessionLocal() as session:
        wrs = WordsRepo(session)
        wrs.add_word(resp[0], resp[1])
        session.commit()
        wrs.add_last_word(resp[0], user_data["user_id"])
    return WordContract(resp[0])
