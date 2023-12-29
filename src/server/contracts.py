from pydantic import BaseModel


class User(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AuthAttributes(BaseModel):
    user_name: str
    user_password: str


class Token(BaseModel):
    token: str
