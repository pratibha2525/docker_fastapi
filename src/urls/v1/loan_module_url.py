from fastapi import APIRouter,Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services.loan_module.controller import Loan_Module
from src.services.loan_module.serializer import UsersSerializer, QuerySerializer

router = APIRouter(prefix="/na_lo")

@router.post("/login/")
async def login(request:UsersSerializer,Authorize:AuthJWT=Depends(),db: Session = Depends(get_db)):
    return await Loan_Module.login(request,Authorize,db)

@router.post("/q/")
async def query(request:QuerySerializer,db: Session = Depends(get_db)):
    return await Loan_Module.query(request,db)
