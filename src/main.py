from fastapi import FastAPI

from src.urls.v1 import ping1_url

app =FastAPI()

app.include_router(ping1_url.router)
