from datetime import datetime, timedelta
from jose import JWTError, jwt
from api.config import settings
from fastapi import HTTPException


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.now()})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def has_role(token: str, role: str):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_role = payload.get("role")

    if role not in user_role:
        return False

    return True
