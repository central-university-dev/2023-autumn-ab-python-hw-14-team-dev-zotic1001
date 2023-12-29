import uuid

from sqlalchemy import insert

from config.settings import app_settings
from typing import Optional
from sqlalchemy.orm import Session
from . import models
from .models import association_table2


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

    def add_last_word(self, word_title, user_id):
        word = self.get_word(word_title)
        smt = insert(association_table2).values(word_id=word.word_id, user_id=user_id)
        self.db.execute(smt)
