from fastapi import FastAPI

import uvicorn
from api.db import get_db, Base, engine
from api.routes.user_router import user_router
from api.routes.auth_router import oauth_router
from api.services.startup_service import startup
from api.routes.static_router import static_router
from api.routes.chat_router import chat_router
from api.routes.ccp_router import ccp_router
from fastapi.staticfiles import StaticFiles
from api.routes.html_router import html_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(user_router)
app.include_router(static_router)
app.include_router(oauth_router)
app.include_router(ccp_router)
app.add_event_handler("startup", startup)
app.include_router(chat_router)
app.include_router(html_router)
app.mount("/cdn", StaticFiles(directory="api/static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4567)
