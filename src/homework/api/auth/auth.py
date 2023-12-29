from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from config.settings import app_settings

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=app_settings.secret_key, lifetime_seconds=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
