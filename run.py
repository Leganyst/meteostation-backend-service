from database.models.models import *
from database.db import engine

from config import app
from routes.auth import auth

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

app.include_router(auth)