import uuid
import jwt
import bcrypt
from config.settings import app_settings
from typing import Optional
from sqlalchemy.orm import Session
from . import models
from src.server.contracts import AuthAttributes


class UsersRepo:
    def __init__(self, db: Session):
        self.db = db

    def check_user(self, auth_attributes: AuthAttributes) -> Optional[models.User]:
        user = (
            self.db.query(models.User)
            .filter(models.User.user_name == auth_attributes.user_name)
            .first()
        )
        if user.password_hash != bcrypt.hashpw(auth_attributes.user_password.encode(), app_settings.salt):
            return None
        else:
            return user

    def add_user(self, user_name: str, user_password: str) -> Optional[models.User]:
        user = models.User(
            user_id=uuid.uuid4(),
            user_name=user_name,
            user_password=user_password
        )
        self.db.add(user)
        return user

    def get_user(self, user_id) -> Optional[models.User]:
        user = (
            self.db.query(models.User)
            .filter(models.User.user_id == user_id)
            .first()
        )
        return Token(token=encoded_jwt)
        if user:
            return user
        else:
            return None

    def add_last_word(self, user_id: int, word: str):
        wr = WordsRepo(self.db)
        word1 = wr.get_word(word)
        self.db.query.execute(
            models.association_table2.insert(), {
                "user_id": user_id,
                "word_id": word1.word_id
            }
        )
