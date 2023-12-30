import logging.config

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import app_settings
from .contracts import Token, AuthAttributes
from db.users import UsersRepo
from sqlalchemy.exc import IntegrityError

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
async def authorization(auth_attributes: AuthAttributes) -> HTTPException | Token:
    try:
        with SessionLocal() as session:
            users_table = UsersRepo(session)
            token = users_table.login_user(auth_attributes)
            if token is None:
                raise HTTPException(status_code=404, detail="User not found")
            return token
    except Exception as error:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from error


@app.post("/register", response_model=Token)
async def register(auth_attributes: AuthAttributes) -> HTTPException | Token:
    try:
        with SessionLocal() as session:
            users_table = UsersRepo(session)
            token = users_table.add_user(auth_attributes)
            session.commit()
        return token
    except IntegrityError as error:
        print(error.params, type(error.params))
        raise HTTPException(
            status_code=409, detail="Account already exists"
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from error
