import logging.config

from faker import Faker
from fastapi import FastAPI, HTTPException, status
from fastapi.openapi.models import Response
from fastapi_users import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.word import wordClient
from db.models import User, Word
from config.settings import app_settings
from .contracts import Token, AuthAttributes, WordContract
from db.users import UsersRepo
from db.words_repo import WordsRepo

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
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)


def login(token: str):
    try:
        decoded_jwt = jwt.decode(token, app_settings.secret_key, algorithms=["HS256"])
        return decoded_jwt
    except jwt.exceptions.DecodeError:
        return None


@app.post("/auth", response_model=Token)
def authorization(auth_attributes: AuthAttributes) -> Token:
    with SessionLocal() as session:
        users_table = UsersRepo(session)
        return users_table.login_user(auth_attributes)


@app.post("/register", response_model=Token)
def register(auth_attributes: AuthAttributes) -> Token:
    with SessionLocal() as session:
        users_table = UsersRepo(session)
        user = users_table.check_user(auth_attributes)
    return Token(message="Hello that", code=1)


@app.get("/word", response_model=WordContract)
def get_word(response: Response):
    user_data = login(response.headers["token"])
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
            headers={"WWW-Authenticate": "Basic"},
        )
    resp = wordClient.get_word_and_translate()
    with SessionLocal() as session:
        WordsRepo(session).add_word(resp[0], resp[1])
        UsersRepo(session).add_last_word(user_data["user_id"], "")
    return WordContract(resp[0])
