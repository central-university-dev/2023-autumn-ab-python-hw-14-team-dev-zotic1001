import bcrypt
from pydantic_settings import BaseSettings


class AppSetting(BaseSettings):

    log_level: str = 'DEBUG'
    db: str = 'postgresql://username:password@db:5432/mydatabase'
    salt: bytes = bcrypt.gensalt()
    secret_key: str = 'secret_key'

    class Config:
        env_prefix = 'APP_'


app_settings = AppSetting()
