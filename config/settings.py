from pydantic_settings import BaseSettings


class AppSetting(BaseSettings):
    log_level: str = 'DEBUG'
    db: str = ''
    secret_key: str = 'secret_key'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_prefix = 'APP_'


app_settings = AppSetting()
