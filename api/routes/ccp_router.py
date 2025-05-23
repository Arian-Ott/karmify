from fastapi import APIRouter, Depends, HTTPException
from api.routes.auth_router import oauth2_scheme, verify_token
from api.services.ccp_service import CCPService
from api.schemas.ccp_schema import CCPReport, CCPReportHTTP
from uuid import UUID

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
    return ccp_service.get_sum_points(payload["uid"])


@ccp_router.post("/infraction")
async def report_infraction(
    infraction: CCPReportHTTP,
    token: str = Depends(oauth2_scheme),
):
    """
    Report an infraction to the CCP.
    Misuse of this API is strictly prohibited and will be reported to the authorities.
    """
    token = verify_token(token)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    infraction = CCPReport(
        reporter=token["uid"],
        category_id=infraction.category_id,
        comment=infraction.comment,
        reportee=infraction.reportee,
    )
    ccp_service.create_ccp_log(infraction)
    return infraction
