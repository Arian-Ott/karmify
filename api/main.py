from fastapi import FastAPI
from api.config import settings
import uvicorn
from api.db import get_db, Base, engine
from api.routes.user_router import user_router
from api.routes.auth_router import oauth_router
from api.services.startup_service import startup
from api.routes.static_router import static_router

app = FastAPI()
app.include_router(user_router)
app.include_router(static_router)
app.include_router(oauth_router)


app.add_event_handler("startup", startup)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4567)
