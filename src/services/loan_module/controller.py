from fastapi import FastAPI, HTTPException,status
from typing import List
from http import HTTPStatus
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.sql import alias

from src.services.loan_module.serializer import UsersSerializer, QuerySerializer

class Settings(BaseModel):
    authjwt_secret_key:str='d1ef9b7d36d6fce56880edbf90c8d6949961db163e4e573984d9675a639e6a8c'

@AuthJWT.load_config
def get_config():
    return Settings()

class Loan_Module():
    
    @classmethod
    async def login(cls,request:UsersSerializer,Authorize,db):
         return Loan_Module(request,Authorize,db)
         
         
    
    @classmethod
    async def query(cls, request:QuerySerializer,db):
           
        final_data = {}
        final_data['reporttype'] = request.reporttype
        final_data['reportrank'] = request.reportrank
        final_data['reportformat'] = request.reportformat
        final_data['usecode'] = request.usecode
        final_data['lendertype'] = request.lendertype
        final_data['lenderstodisplay'] = request.lenderstodisplay
        final_data['addgroup'] = request.addgroup
        final_data['pmmnonpmm'] = request.pmmnonpmm
        final_data['refionly'] = request.refionly
        final_data['loantypessubbypass'] = request.loantypessubbypass
        final_data['loanmin'] = request.loanmin
        final_data['loanmax'] = request.loanmax
        final_data['nmlsid'] = request.nmlsid
        final_data['summarizeby'] = request.summarizeby
        final_data['allowcustomregion'] = request.allowcustomregion
        final_data['customregion'] = request.customregion
        final_data['state'] = request.state
        final_data['county'] = request.county
        final_data['citytown'] = request.citytown
        final_data['zipcode'] = request.zipcode
        final_data['censustract'] = request.censustract
        final_data['year'] = request.year
        final_data['period'] = request.period
        final_data['reporting'] = request.reporting
        final_data['lt'] = request.lt
        final_data['uid'] = request.uid
        final_data['tmp_inner'] = request.tmp_inner
        final_data['ifilter'] = request.ifilter
        final_data['report_ary'] = request.report_ary
        final_data['reportheader_ary'] = request.reportheader_ary
        final_data['reportfull_ary'] = request.reportfull_ary
        final_data['sql'] = request.sql
        final_data['tsql'] = request.tsql
        final_data['report'] = request.report
        
        return final_data