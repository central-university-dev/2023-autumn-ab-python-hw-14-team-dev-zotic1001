import uuid
import jwt
import bcrypt
from config.settings import app_settings
from typing import Optional
from sqlalchemy.orm import Session
from . import models
from src.server.contracts import AuthAttributes, Token


class UsersRepo:
    def __init__(self, db: Session):
        self.db = db

    def login_user(self, auth_attributes: AuthAttributes) -> Optional[Token]:
        user = (
            self.db.query(models.User)
            .filter(models.User.user_name == auth_attributes.user_name)
            .first()
        )
        if user.password_hash != bcrypt.hashpw(auth_attributes.user_password.encode(), app_settings.salt):
            return None
        else:
            encoded_jwt = jwt.encode(
                {'user_id': user.user_id, 'user_name': user.user_name},
                app_settings.secret_key,
                algorithm='HS256',
            )
            return Token(token=encoded_jwt)

    def add_user(self, auth_attributes: AuthAttributes) -> Optional[Token]:
        user = models.User(
            user_id=uuid.uuid4(),
            user_name=auth_attributes.user_name,
            password_hash=auth_attributes.user_password
        )
        self.db.add(user)
        encoded_jwt = jwt.encode(
            {'user_id': str(user.user_id), 'user_name': user.user_name},
            app_settings.secret_key,
            algorithm='HS256',
        )
        return Token(token=encoded_jwt)
