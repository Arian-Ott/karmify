from fastapi import FastAPI
from api.config import settings
import uvicorn
from api.db import get_db, Base, engine


app = FastAPI()


def startup():
    """Startup event handler."""
    if settings.DEBUG:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


app.add_event_handler("startup", startup)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4567)
