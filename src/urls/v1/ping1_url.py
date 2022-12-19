# from fastapi-boilerplate.src.urls import controller\
from fastapi import APIRouter
from src.services.ping1.controller import Ping

router = APIRouter(prefix="/ping")

@router.get("/")
async def ping():
    return await Ping.ping()

