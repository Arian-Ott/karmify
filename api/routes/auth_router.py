from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api.services.jwt import create_access_token, verify_token
from api.services.user_service import User
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

oauth_router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@oauth_router.post("/token")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    target_url: str = None,
):
    user_data = User.authenticate_user(form_data.username, form_data.password)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Make sure user_data is a dict or Pydantic model, not a detached ORM object
    access_token = create_access_token(
        data={
            "sub": user_data["username"],
            "role": User.get_roles(user_data["username"]),
            "uid": user_data["user_id"],
        }
    )
    if target_url:
        # If a target URL is provided, redirect to it
        response = RedirectResponse(
            url="/" + target_url, status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        # Otherwise, return a JSON response
        response = JSONResponse(
            content={"access_token": access_token, "token_type": "bearer"}
        )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600,  # 1 hour
        expires=3600,
        secure=True,  # set to False for local dev, True in production
        samesite="Lax",
        path="/",
    )
    return response


@oauth_router.get("/logout")
async def logout():
    response = RedirectResponse(
        url="/login", status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("access_token")
    return response
    


@oauth_router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"user": payload["sub"]}


@oauth_router.delete("/me")
async def delete_current_user(
    response: Response,
    token: str = Depends(oauth2_scheme),
):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    if "admin" in payload["role"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin cannot delete self"
        )
    user = User.get_by_username(payload["sub"])

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    User.delete_user(payload["uid"])
    response.delete_cookie("access_token")

    return {"detail": "User deleted"}
