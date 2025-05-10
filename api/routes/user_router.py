from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.user_schema import UserBase
from api.services.user_service import User

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/register",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Bad Request"},
        500: {"description": "Internal Server Error"},
    },
)
async def register_user(user: UserBase):
    user_service = User()
    user_service.set_schema(user)
    try:
        user = user_service.create_user()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user
