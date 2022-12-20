from fastapi import APIRouter,Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services.user_login1.controller import Users_Module
from src.services.user_login1.serializer import UsersSerializer, QuerySerializer


##### MARKET SHARE MODULE (login, run_query, save_query, load_query) #####

router = APIRouter(prefix="/fa_marketshare")

@router.post("/login/")
async def login(request:UsersSerializer,Authorize:AuthJWT=Depends(),db: Session = Depends(get_db)):
    return await Users_Module.login(request,Authorize,db)

@router.post("/q/")
async def query(request:QuerySerializer,db: Session = Depends(get_db)):
    return await Users_Module.query(request,db)

@router.post("/saveq/")
async def saveq():
    return await Users_Module.saveq()

@router.get("/listq/")
async def savelistq():
    return await Users_Module.savelistq()

@router.post("/saveqname/")
async def save_q_name():
    return await Users_Module.save_q_name()
