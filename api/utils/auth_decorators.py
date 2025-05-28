from fastapi.responses import RedirectResponse
from functools import wraps
from fastapi import Request
from datetime import datetime, timedelta
from fastapi.exceptions import HTTPException
from api.services.jwt import verify_token, create_access_token
from api.config import settings


def protected_route(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            resp = RedirectResponse(url="/login", headers={"X-Messages": "You must be logged in to access this page."})
            resp.set_cookie("messages", "You must be logged in to access this page.", httponly=True, max_age=5, expires=5, secure=False, samesite="Lax", path="/")
            return resp

        user = verify_token(token)
        if not user:
            resp =  RedirectResponse(url="/login")
            resp.set_cookie("messages", "Invalid token. Please log in again.", httponly=True, max_age=5, expires=5, secure=False, samesite="Lax", path="/")
            return resp

        exp = user.get("exp")
        if not exp or datetime.fromtimestamp(exp) < datetime.now():
            resp = RedirectResponse(url="/login", headers={"X-Messages": "Session expired. Please log in again."})
            resp.set_cookie("messages", "Session expired. Please log in again.", httponly=True, max_age=5, expires=5, secure=False, samesite="Lax", path="/")
            return resp

        if datetime.fromtimestamp(exp) < datetime.now() + timedelta(minutes=10):
            new_token = create_access_token(
                data={
                    "sub": user["sub"],
                    "role": user.get("role", []),
                    "uid": user["uid"],
                },
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            response = RedirectResponse(url=request.url.path)
            response.set_cookie("access_token", new_token, httponly=True, max_age=3600, expires=3600, secure=False, samesite="Lax", path="/")
            return response

        request.state.user = user
        return await func(request, *args, **kwargs)

    return wrapper


def requires_role(func, role):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.cookies.get("access_token")

        user = verify_token(token)
        if not "role" in user.keys():
            raise HTTPException(status_code=402, detail="Not auth")
        if not role in user["role"]:
            raise HTTPException(status_code=418, detail="I'M A TEAPOT")
        return await func(request, *args, **kwargs)

    return wrapper
