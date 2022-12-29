from fastapi import APIRouter,Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services.user_login1.controller import Users_Module
from src.services.user_login1.serializer import UsersSerializer, QuerySerializer, SaveSerializer


##### MARKET SHARE MODULE (login, run_query, save_query, load_query) #####

router = APIRouter(prefix="/fa_marketshare")

@router.post("/login/")
async def login(request:UsersSerializer,Authorize:AuthJWT=Depends(),db: Session = Depends(get_db)):
    return await Users_Module.login(request,Authorize,db)

@router.post("/q/")
async def query(request:QuerySerializer,db: Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    return await Users_Module.query(request,db,Authorize)

@router.post("/saveq/")
async def saveq(request:SaveSerializer,db: Session = Depends(get_db)):
    return await Users_Module.saveq(request,db)

@router.get("/listq/")
async def savelistq():
    return await Users_Module.savelistq()

@router.post("/saveqname/")
async def save_q_name():
    return await Users_Module.save_q_name()

#####
@router.post("/xls/")
async def xls():
    pass

@router.post("/txt/")
async def txt():
    pass

@router.post("/csv/")
async def csv():
    pass
