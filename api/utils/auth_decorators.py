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
            return RedirectResponse(url="/login")

        user = verify_token(token)
        if not user:
            return RedirectResponse(url="/login")

        exp = user.get("exp")
        if not exp or datetime.fromtimestamp(exp) < datetime.now():
            return RedirectResponse(url="/login")


        if datetime.fromtimestamp(exp) < datetime.now() + timedelta(minutes=10):
            new_token = create_access_token(
                data={
                    "sub": user["sub"],
                    "role": user.get("role", []),
                    "uid": user["uid"],
                },
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            response = RedirectResponse(url=request.url.path)
            response.set_cookie("access_token", new_token, httponly=True)
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
