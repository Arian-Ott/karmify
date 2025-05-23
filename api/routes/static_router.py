from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
from uuid import UUID
import zlib
import os
from api.config import settings
from api.services.importing_service import handler
from api.routes.auth_router import oauth2_scheme
from api.services.jwt import verify_token

static_router = APIRouter(prefix="/static", tags=["static"])


DEFAULT_IMG = os.path.join(settings.ASSET_DIR, "nnonftscam.png")


def checksum_img(image_bytes: bytes) -> str:
    """Generate a CRC32 checksum of raw image bytes."""
    return f"{zlib.crc32(image_bytes) & 0xFFFFFFFF:08x}"


@static_router.post(
    "/u/{user_id}",
    responses={
        401: {"description": "Unauthorized. The user could not be authorized"},
        201: {"description": "Created profile picture"},
    },
)
async def set_pfp(
    user_id: str,
    image: UploadFile,
    token: str = Depends(oauth2_scheme),
):
    data = verify_token(token)

    if data is None or data.get("uid") != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    image_bytes = await image.read()

    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    filename = f"{user_id}.webp"
    path = os.path.join(settings.ASSET_DIR, filename)

    if not os.path.exists(path):
        img.save(path, "WEBP", optimize=True, quality=85)

    return {"message": "Profile picture uploaded"}


@static_router.get("/u/{user_id}")
async def get_pfp(user_id: str):
    path = os.path.join(settings.ASSET_DIR, f"{user_id}.webp")
    if not os.path.exists(path):
        return FileResponse(DEFAULT_IMG)
    return FileResponse(path)


@static_router.delete("/u/{user_id}")
async def delete_pfp(user_id, token: str = Depends(oauth2_scheme)):
    token = verify_token(token)
    if not token:
        raise HTTPException(401)
    if not token["uid"] == user_id:
        raise HTTPException(401)
    if not os.path.exists(settings.ASSET_DIR + f"/{user_id}.webp"):
        raise HTTPException(404, detail="Image not found")
    os.remove(settings.ASSET_DIR + f"/{user_id}.webp")
    return "image deleted"


@static_router.post("/bulk_import")
async def bulk_import(
    token: str = Depends(oauth2_scheme),
):
    data = verify_token(token)
    if data is None or "admin" not in data.get("role"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    await handler()
    return {"message": "Bulk import completed"}
