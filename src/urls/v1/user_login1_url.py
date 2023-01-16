from fastapi import APIRouter,Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services.user_login1.controller import Users_Module
from src.services.user_login1.serializer import UsersSerializer, QuerySerializer, SaveSerializer, CsvSerializer, LoadSerializer, DeleteSerializer, UpdateSerializer,LogoutSerializer


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

@router.post("/updateq/")
async def updateq(request:UpdateSerializer,db: Session = Depends(get_db)):
    return await Users_Module.updateq(request,db)


@router.post("/listq/")
async def listq(request:LoadSerializer,db: Session = Depends(get_db)):
    return await Users_Module.listq(request,db)

@router.post("/deleteq/")
async def deleteq(request:DeleteSerializer,db: Session = Depends(get_db)):
    return await Users_Module.deleteq(request,db)

@router.post("/logoutq/")
async def logoutq(request:LogoutSerializer,db: Session = Depends(get_db)):
    return await Users_Module.logoutq(request,db)

#####



@router.post("/csv/")
async def csv(request:CsvSerializer):
    return await Users_Module.csv(request)

@router.post("/txt/")
async def txt(request:CsvSerializer):
    return await Users_Module.txt(request)

@router.post("/xls/")
async def xls(request:CsvSerializer):
    return await Users_Module.xls(request)

@router.post("/pdf/")
async def pdf(request:CsvSerializer):
    return await Users_Module.pdf(request)
