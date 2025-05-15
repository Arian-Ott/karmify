from fastapi import APIRouter, Depends, HTTPException
from api.routes.auth_router import oauth2_scheme
from api.services.jwt import has_role, verify_token

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/<user_id>/message")
@chat_router.get("/messages")
async def get_messages(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")


# TODO: Implement the logic to get messages
# TODO: Implement logic to block users
# TODO: Implement logic to encrypt messages (not MVP relevant)
