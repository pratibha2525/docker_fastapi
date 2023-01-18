from fastapi import FastAPI

from src.db import models
from src.db.database import engine,SessionLocal
from src.urls.v1 import ping1_url, user_login1_url,loan_module_url

from fastapi.middleware.cors import CORSMiddleware

app =FastAPI() 

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(engine)

app.include_router(ping1_url.router)

## MSM

app.include_router(user_login1_url.router)

## LOAN

app.include_router(loan_module_url.router)
