from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from api.routes.auth_router import oauth2_scheme, verify_token
from api.services.ccp_service import CCPService
from api.schemas.ccp_schema import CCPReport, CCPReportHTTP
from uuid import UUID
from api.utils.auth_decorators import protected_route
from fastapi import Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse

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
            "points": 999999
        }  # Hardcoded, since the admin will always have 999.999 points.
    return ccp_service.get_sum_points(payload["uid"])


@ccp_router.post("/infraction")
@protected_route
async def report_infraction(
    request: Request,
    reportee: str = Form(...),
    category_id: int = Form(...),
    comment: str = Form(...),
):
    """
    Report an infraction to the CCP.
    Misuse of this API is strictly prohibited and will be reported to the authorities.
    """
    token = verify_token(request.cookies.get("access_token"))

    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    infraction = CCPReport(
        reporter=token["uid"],
        category_id=category_id,
        comment=comment,
        reportee=reportee,
    )
    ccp_service.create_ccp_log(infraction)
    response = RedirectResponse(
        url="/dashboard",
        status_code=303,
        headers={"X-Messages": "Infraction reported successfully"},
    )
    response.set_cookie(
        key="access_token",
        value=request.cookies.get("access_token"),
        httponly=True,
        max_age=3600,  # 1 hour
        expires=3600,
        secure=True,  # set to False for local dev, True in production
        samesite="Lax",
        path="/",
    )
    return response
