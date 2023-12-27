from sqlalchemy import Column, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = password = Column(String)
