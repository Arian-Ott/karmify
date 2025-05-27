from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends
from api.config import templates
from api.routes.auth_router import oauth2_scheme
from api.services.jwt import verify_token
from api.utils.auth_decorators import protected_route
import requests
from api.services.ccp_service import CCPService
html_router = APIRouter(tags=["html"])




@html_router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """
    Render the index page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@html_router.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    """
    Render the signup page.
    """
    return templates.TemplateResponse("signup.html", {"request": request})


@html_router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    """
    Render the login page.
    """
    if request.cookies.get("access_token"):
        if not verify_token(request.cookies.get("access_token")):
            response = RedirectResponse(url="/login", status_code=303)
            response.delete_cookie("access_token")
            return response
        else:
            # If the user is already logged in, redirect to the dashboard
            return RedirectResponse(url="/dashboard", status_code=303)
    if request.headers.get("X-Messages"):
        return templates.TemplateResponse(
            "login.html", {"request": request, "messages": ["Login successful"]}
        )
    return templates.TemplateResponse("login.html", {"request": request})


@html_router.get(
    "/dashboard",
)
@protected_route
async def get_dashboard(request: Request):
    """
    Render the dashboard page.
    """
    ccp_service = CCPService()
    user_id = verify_token(request.cookies.get("access_token"))["uid"]
    karma_list =  ccp_service.get_ccp_logs(user_id)
    
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": request.state.user, "karma_log": karma_list}
    )


@html_router.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    """
    Render the about page.
    """
    return templates.TemplateResponse("about.html", {"request": request})

@html_router.get("/chat", response_class=HTMLResponse)
async def get_chat(request: Request):
    """
    Render the chat page.
    """
    
    return templates.TemplateResponse("chat.html", {"request": request})

@html_router.get("/imprint", response_class=HTMLResponse)
async def get_imprint(request: Request):
    """
    Render the imprint page.
    """
    return templates.TemplateResponse("impressum.html", {"request": request})