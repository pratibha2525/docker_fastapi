from fastapi import FastAPI, HTTPException,status
from typing import List
from http import HTTPStatus
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.sql import alias

from src.services.loan_module.serializer import Lo_UsersSerializer, SaveSerializer, UpdateSerializer,DeleteSerializer,LoadSerializer,CsvSerializer
from src.services.loan_module.schema import User_Schema,SaveQuery,DeleteQuery,ListQuery
from src.utils.response_utils import ResponseUtil
from src.config.constant import UserConstant
from src.utils.logger_utils import LoggerUtil


# class Settings(BaseModel):
#     authjwt_secret_key:str='d1ef9b7d36d6fce56880edbf90c8d6949961db163e4e573984d9675a639e6a8c'

# @AuthJWT.load_config
# def get_config():
#     return Settings()

class Loan_Module():
    
    @classmethod
    async def login(cls,request:Lo_UsersSerializer,Authorize,db):
        try:
            user = User_Schema.user_login(request.usr_email,db)
        except Exception as e:
            return ResponseUtil.error_response(message = UserConstant.ERROR_MESSAGE)

        try:
            if user != None:
                LoggerUtil.info(UserConstant.USER_GET)
                if (user.usr_username==request.usr_username) and (user.usr_password==request.usr_password):
                    access_token=Authorize.create_access_token(subject=user.usr_id)
                    refresh_token=Authorize.create_refresh_token(subject=user.usr_id)
                    # expires = datetime.timedelta(days=1)
                    # token = Authorize.create_access_token(subject="test",expires_time=expires)
                    # return {"token": token}
                    data = {"access_token": access_token,"refresh_token": refresh_token}
                    LoggerUtil.info(UserConstant.LOGIN_SUCCESS)
                    return ResponseUtil.success_response(data,message=UserConstant.LOGIN_SUCCESS)
                else:
                    LoggerUtil.info(UserConstant.USER_PASSWORD_INVALID)
                    return ResponseUtil.success_response(message=UserConstant.USER_PASSWORD_INVALID)
            else:
                LoggerUtil.info(UserConstant.USER_NOT_FOUND)
                return ResponseUtil.success_response(message=UserConstant.USER_NOT_FOUND)

        except Exception as e:
            LoggerUtil.logException(UserConstant.ERROR_MESSAGE , exception = str(e))
            return ResponseUtil.error_response(message =UserConstant.ERROR_MESSAGE)
         
    # @classmethod
    # async def query(cls, request:QuerySerializer,db):
           
    #     final_data = {}
    #     final_data['reporttype'] = request.reporttype
    #     final_data['reportrank'] = request.reportrank
    #     final_data['reportformat'] = request.reportformat
    #     final_data['usecode'] = request.usecode
    #     final_data['lendertype'] = request.lendertype
    #     final_data['lenderstodisplay'] = request.lenderstodisplay
    #     final_data['addgroup'] = request.addgroup
    #     final_data['pmmnonpmm'] = request.pmmnonpmm
    #     final_data['refionly'] = request.refionly
    #     final_data['loantypessubbypass'] = request.loantypessubbypass
    #     final_data['loanmin'] = request.loanmin
    #     final_data['loanmax'] = request.loanmax
    #     final_data['nmlsid'] = request.nmlsid
    #     final_data['summarizeby'] = request.summarizeby
    #     final_data['allowcustomregion'] = request.allowcustomregion
    #     final_data['customregion'] = request.customregion
    #     final_data['state'] = request.state
    #     final_data['county'] = request.county
    #     final_data['citytown'] = request.citytown
    #     final_data['zipcode'] = request.zipcode
    #     final_data['censustract'] = request.censustract
    #     final_data['year'] = request.year
    #     final_data['period'] = request.period
    #     final_data['reporting'] = request.reporting
    #     final_data['lt'] = request.lt
    #     final_data['uid'] = request.uid
    #     final_data['tmp_inner'] = request.tmp_inner
    #     final_data['ifilter'] = request.ifilter
    #     final_data['report_ary'] = request.report_ary
    #     final_data['reportheader_ary'] = request.reportheader_ary
    #     final_data['reportfull_ary'] = request.reportfull_ary
    #     final_data['sql'] = request.sql
    #     final_data['tsql'] = request.tsql
    #     final_data['report'] = request.report
        
    #     return final_data

    @classmethod
    async def saveq(cls,request:SaveSerializer,db):
        save_query = SaveQuery.save_query(request,db)

        final_data = {}
        final_data["q_id"] = save_query.q_id
        return ResponseUtil.success_response(final_data,message="Success")

    @classmethod
    async def updateq(cls,request:UpdateSerializer,db):

        update_query = SaveQuery.update_query(request,db)
        final_data = {}
        final_data["q_id"] = request.q_id
        final_data["usr_id"] = request.usr_id
        final_data["q_name"] = request.q_name

        return ResponseUtil.success_response(final_data,message="Success")

    @classmethod
    async def deleteq(cls,request:DeleteSerializer,db):
        delete_query = DeleteQuery.delete_query(request,db)

        final_data = {}
        final_data["q_id"] = request.q_id
        final_data["usr_id"] = request.usr_id
        final_data["countaffected"] = 1
        return ResponseUtil.success_response(final_data,message="Success")

    @classmethod
    async def listq(cls,request:LoadSerializer,db):
        liste_query = ListQuery.list_query(request,db)
        final_list_data = []

        for list_data in liste_query:
            data = {}
            data["q_id"] = list_data.q_id
            data["usr_id"] = list_data.usr_id
            data["q_name"] = list_data.q_name
            data["q_create_ts"] = str(list_data.q_create_ts)
            data["q_lastmod"] = str(list_data.q_lastmod)
            data["q_parms"] = list_data.q_parms
            final_list_data.append(data)

        final_data = {}
        final_data["data"] = final_list_data

        return ResponseUtil.success_response(final_data,message="Success")

#### CSV, PDF, XLZ, TXT

    @classmethod
    async def csv(cls,request:CsvSerializer):
        return "i am CSV"

    @classmethod
    async def txt(cls,request:CsvSerializer):
        return "i am TXT"

    @classmethod
    async def xls(cls,request:CsvSerializer):
        return "i am xls"

    @classmethod
    async def pdf(cls,request:CsvSerializer):
        return "i am pdf"
