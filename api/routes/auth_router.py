from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api.services.jwt import create_access_token, verify_token
from api.services.user_service import User

oauth_router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@oauth_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
    return {"access_token": access_token, "token_type": "bearer"}


@oauth_router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"detail": "Logged out (simulated, token not really invalidated)"}


@oauth_router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"user": payload["sub"]}
