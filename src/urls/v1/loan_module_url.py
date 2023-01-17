from fastapi import APIRouter,Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services.loan_module.controller import Loan_Module
from src.services.loan_module.serializer import Lo_UsersSerializer, SaveSerializer, UpdateSerializer,DeleteSerializer,LoadSerializer,CsvSerializer

router = APIRouter(prefix="/na_lo")

@router.post("/login/")
async def login(request:Lo_UsersSerializer,Authorize:AuthJWT=Depends(),db: Session = Depends(get_db)):
    return await Loan_Module.login(request,Authorize,db)

# @router.post("/q/")
# async def query(request:QuerySerializer,db: Session = Depends(get_db)):
#     return await Loan_Module.query(request,db)

@router.post("/saveq/")
async def saveq(request:SaveSerializer,db: Session = Depends(get_db)):
    return await Loan_Module.saveq(request,db)

@router.post("/updateq/")
async def updateq(request:UpdateSerializer,db: Session = Depends(get_db)):
    return await Loan_Module.updateq(request,db)

@router.post("/deleteq/")
async def deleteq(request:DeleteSerializer,db: Session = Depends(get_db)):
    return await Loan_Module.deleteq(request,db)

@router.post("/listq/")
async def listq(request:LoadSerializer,db: Session = Depends(get_db)):
    return await Loan_Module.listq(request,db)

### CSV, TXT, XLS, PDF

@router.post("/csv/")
async def csv(request:CsvSerializer):
    return await Loan_Module.csv(request)

@router.post("/txt/")
async def txt(request:CsvSerializer):
    return await Loan_Module.txt(request)

@router.post("/xls/")
async def xls(request:CsvSerializer):
    return await Loan_Module.xls(request)

@router.post("/pdf/")
async def pdf(request:CsvSerializer):
    return await Loan_Module.pdf(request)