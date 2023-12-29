from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)


class Word(Base):
    __tablename__ = "words"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String)
    category = Column(ForeignKey("categories.id"))


class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String)
