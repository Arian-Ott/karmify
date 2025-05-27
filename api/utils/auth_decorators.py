from fastapi import Request
from fastapi.responses import RedirectResponse
from functools import wraps
from fastapi.exceptions import HTTPException
from api.services.jwt import verify_token


def protected_route(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.cookies.get("access_token")
        if token is None:
            return RedirectResponse(url="/login")
        user = verify_token(token)

        if user is None:
            return RedirectResponse(url="/login")

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
