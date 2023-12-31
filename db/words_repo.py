import uuid

from sqlalchemy import insert, select, update

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
            word_id=uuid.uuid4(),
            title=word,
            translation=translation
        )
        self.db.add(word)
        self.db.commit()
        return word

    def get_word(self, word_title: str) -> Optional[models.Word]:
        word = self.db.query(models.Word).filter(models.Word.title == word_title).first()
        return word

    def get_translation_by_word_title(self, word_title: str) -> str:
        word = self.db.query(models.Word).filter(models.Word.title == word_title).first()
        return word.translation

    def get_word_by_id(self, word_id):
        word = self.db.query(models.Word).filter(models.Word.word_id == word_id).first()
        return word
    def add_last_word(self, word_title, user_id):
        word = self.get_word(word_title)
        smt = select(association_table2).where(association_table2.c.users == user_id)
        res = self.db.execute(smt)
        if len(list(res)) == 0:
            upd = insert(association_table2).values(words=word.word_id, users=user_id)
            self.db.execute(upd)
            self.db.commit()
            return
        upd = update(association_table2).where(association_table2.c.users == user_id).values(words=word.word_id)
        self.db.execute(upd)
        self.db.commit()

    def get_user_last_word(self, user_id):
        smt = select(association_table2).where(association_table2.c.users == user_id)
        res = self.db.execute(smt)
        word_id = list(res)[0][0]
        if word_id is None:
            return None
        return self.get_word_by_id(word_id).title
