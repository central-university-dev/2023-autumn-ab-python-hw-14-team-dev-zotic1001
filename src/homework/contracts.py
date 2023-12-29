from pydantic import BaseModel


class User(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Message(BaseModel):
    message: str
    code: int
