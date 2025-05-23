from fastapi import APIRouter, Depends, HTTPException
from api.routes.auth_router import oauth2_scheme, verify_token
from api.services.ccp_service import CCPService

ccp_router = APIRouter(prefix="/ccp", tags=["ccp"])

ccp_service = CCPService()


@ccp_router.get("/china_points")
async def get_china_points(token: str = Depends(oauth2_scheme)):
    """
    Get all points in China issued by the CCP.
    Misuse of this API is strictly prohibited and will be reported to the authorities.
    Misuse = -99999 china points.
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    if "admin" in payload["role"]:
        return {
            "points": 99999
        }  # Hardcoded, since the admin will always have 99999 points.
    return {"points": ccp_service.get_sum_points(payload["uid"])}
