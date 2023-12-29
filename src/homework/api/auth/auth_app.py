from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .auth import auth_backend
from db.models import User
from .manager import get_user_manager
from .schemas import UserRead, UserCreate

auth_app = FastAPI(
    title="Auth Router"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_app.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

auth_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

current_user = fastapi_users.current_user()

@auth_app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"
