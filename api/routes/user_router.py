from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.user_schema import UserBase
from api.services.user_service import User
from api.services.jwt import has_role
from api.routes.auth_router import oauth2_scheme

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


@user_router.get(
    "/",
    responses={
        200: {
            "description": "Users retrieved successfully",
            401: {"description": "Unauthorised, admin only"},
        }
    },
)
async def get_all_users(token: str = Depends(oauth2_scheme)):
    if not has_role(token, "admin"):
        raise HTTPException(status_code=403, detail="Not authorised")

    user_service = User()
    try:
        users = user_service.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return users
