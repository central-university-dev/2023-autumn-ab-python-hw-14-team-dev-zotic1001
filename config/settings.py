from pydantic_settings import BaseSettings


class AppSetting(BaseSettings):

    log_level: str = 'DEBUG'
    db: str = 'postgresql://username:password@db:5432/mydatabase'
    salt: str = '<PASSWORD>'.encode()

    class Config:
        env_prefix = 'APP_'


app_settings = AppSetting()
