from database.models.models import *
from database.db import engine

from config import app
from routes.auth import auth
from routes.users import user_api
from routes.devices import device_api

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

app.include_router(auth)
app.include_router(user_api)
app.include_router(device_api)