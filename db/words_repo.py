import uuid
import bcrypt
from config.settings import app_settings
from typing import Optional
from sqlalchemy.orm import Session
from . import models


class WordsRepo:
    def __init__(self, db: Session):
        self.db = db

    def add_word(self, word: str, translation: str) -> Optional[models.Word]:
        word = models.Word(
            title=word,
            translation=translation
        )
        self.db.add(word)
        return word

    def get_word(self, word_title: str) -> Optional[models.Word]:
        word = models.Word(
            self.db.query(models.Word)
            .filter(models.Word.title == word_title)
            .first()
        )
        return word

    def get_translation(self, word_title: str) -> str:
        word = models.Word(
            self.db.query(models.Word)
            .filter(models.Word.title == word_title)
            .first()
        )
        return word.translation

