from pydantic_settings import BaseSettings


class AppSetting(BaseSettings):

    log_level: str = 'DEBUG'
    db: str = 'postgresql://username:password@db:5432/mydatabase'
    api_key: str = '52dc615079msh293b0674f650d42p1b81fajsncdb66021277d'
    class Config:
        env_prefix = 'APP_'


app_settings = AppSetting()
