from fastapi import FastAPI, HTTPException,status
from typing import List
from http import HTTPStatus
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.sql import alias
from fastapi import APIRouter,Depends
from datetime import datetime

from src.utils.response_utils import ResponseUtil
from src.db.models import Users, NDTnewMortgage,U_Queries
from src.utils.sso import generate_token
from src.config.constant import UserConstant
from src.utils.logger_utils import LoggerUtil
from src.services.user_login1.schema import User_Schena,Query_Schema
from src.services.user_login1.serializer import QuerySerializer, UsersSerializer,SaveSerializer


class Settings(BaseModel):
    authjwt_secret_key:str='d1ef9b7d36d6fce56880edbf90c8d6949961db163e4e573984d9675a639e6a8c'

@AuthJWT.load_config
def get_config():
    return Settings()

class Helper():

    @classmethod
    def loan_types_sub_convert(cls,loan_types_sub):
        loan_types_sub_convert = []
        for loan_type in loan_types_sub:
            if loan_type == "Home Equity Loan":
                loan_types_sub = "mHMEQ"
                loan_types_sub_convert.append(loan_types_sub)
            else:
                loan_types_sub = "m" + loan_type
                loan_types_sub_convert.append(loan_types_sub)

        return loan_types_sub_convert

##### MARKET SHARE MODULE (login, run_query, save_query, load_query) #####

class Users_Module():

    @classmethod
    async def login(cls,request:UsersSerializer,Authorize,db):
        try:
            user = User_Schena.user_login(request.usr_email,db)
        except Exception as e:
            return ResponseUtil.error_response(message = UserConstant.ERROR_MESSAGE)

        try:
            if user != None:
                LoggerUtil.info(UserConstant.USER_GET)
                if (user.usr_username==request.usr_username) and (user.usr_password==request.usr_password):
                    access_token=Authorize.create_access_token(subject=user.usr_username)
                    refresh_token=Authorize.create_refresh_token(subject=user.usr_username)
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


    @classmethod
    async def query(cls, request:QuerySerializer,db,Authorize):

        # try:
        #     Authorize.jwt_required()
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

        # current_user=Authorize.get_jwt_subject()

        data = Query_Schema.master_query(db)

        if request.summarizeby == "State Level":
            state = []
            for state_value in request.state:
                state.append(state_value["state"])
            data = Query_Schema.query(data,state=request.state)
        elif request.summarizeby == "County Level":
            county = []
            state = []
            for county_value in request.county:
                county.append(county_value["county"])
            
            for state_value in request.state:
                state.append(state_value["state"])
            data = Query_Schema.query(data,county=county,state=state)

        if request.year != []:
            data = Query_Schema.query(data,year=request.year)

        if request.lenders != []:
            data = Query_Schema.query(data,lenders=request.lenders)

        if request.loantypessub != []:
            loantypessub = Helper.loan_types_sub_convert(request.loantypessub)
            data = Query_Schema.query(data,loantypessub=loantypessub)

        # data = data.all()
        craeted_at = str(datetime.now())
        proprty_type = request.usecode["usecodegroup"] + request.usecode["usecode"]

        reportheader_ary = []
        if request.summarizeby == "State Level":
            state_str = ' ,'.join([str(elem) for elem in state])
            regions = f"All Regions in {state_str}"

        elif request.summarizeby == "County Level":
            county_lst = []
            for i in request.county:
                county_lst.append(i["county"] + " County")
                county_lst.append(i["state"] +" ")
            county_str = ' ,'.join([str(elem) for elem in county_lst])
            regions = county_str

        for year in request.year:
            for period in request.period:
                ary = []
                ary.append(proprty_type)
                ary.append("Skyward Techno.")
                ary.append(regions)
                ary.append(f"{year} {period}")
                ary.append(request.reportrank)
                ary.append(craeted_at)
                reportheader_ary.append(ary)

        subheader = ["All Mortgages","Purchase Mortgages","Non Purchase Mortgages",f"Mkt Shr by {request.reportrank}(%)"]
        subtitle = ["Lender Name","All","P","N","Total Value","Total Number","Total Value","Total Number","Total Value","Total Number","All","P","NP"]

        final_data = {}
        final_data["reporttype"] = request.reporttype
        final_data["reportrank"] = request.reportrank
        final_data["reportformat"] = request.reportformat
        final_data["usecode"] = request.usecode
        final_data["loanpurpose"] = request.loanpurpose
        final_data["lendertype"] = request.lendertype
        final_data["lenderstodisplay"] = request.lenderstodisplay
        final_data["lenders"] = request.lenders
        final_data["ltext"] = request.ltext
        final_data["loantypes"] = request.loantypes
        final_data["loantypessub"] = request.loantypessub
        final_data["refionly"] = request.refionly
        final_data["excl_usahud"] = request.excl_usahud
        final_data["loantypessubbypass"] = request.loantypessubbypass
        final_data["loanmin"] = request.loanmin
        final_data["loanmax"] = request.loanmax
        final_data["summarizeby"] = request.summarizeby
        final_data["state"] = request.state
        final_data["county"] = request.county
        final_data["citytown"] = request.citytown
        final_data["zipcode"] = request.zipcode
        final_data["censustract"] = request.censustract
        final_data["year"] = request.year
        final_data["period"] = request.period
        final_data["reporting"] = request.reporting
        final_data["lt"] = request.lt
        final_data["brokerlenderbypass"] = request.brokerlenderbypass
        final_data["uid"] = ""
        final_data["lenderflag"] = ""
        if  len(request.lenders) == 0:
            final_data["lenderlen"] = len(request.lenders)
        else:
            final_data["lendernamearray"] = request.lenders
            final_data["lenderlen"] = len(request.lenders)

        final_data["ifilter"] = ""
        final_data["report_ary"] = ""
        final_data["reportheader_ary"] = reportheader_ary

        if request.brokerlenderbypass == True:
            final_data["brokerflaginside"] = True
            final_data["brokerflag"] = True
        else:
            final_data["brokerflaginside"] = False
            final_data["brokerflag"] = False

        final_data["sql"] = ""
        final_data["report"] = ""
        final_data["subheader"] = subheader
        final_data["subtitle"] = subtitle

        return ResponseUtil.success_response(final_data,message="Success")
    

                
    @classmethod
    async def saveq(cls, request:SaveSerializer,db):
        print("i am request",(request.usecod))
        save_query = Query_Schema.saveq(request=str(request),db=db)
        return save_query


    @classmethod
    async def savelistq(cls):
        pass

    @classmethod
    async def save_q_name(cls):
        pass
