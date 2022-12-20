from fastapi import FastAPI

from src.db import models
from src.db.database import engine,SessionLocal
from src.urls.v1 import ping1_url, user_login1_url

app =FastAPI() 

models.Base.metadata.create_all(engine)

app.include_router(ping1_url.router)

## MSM

app.include_router(user_login1_url.router)
