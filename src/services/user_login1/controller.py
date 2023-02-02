import csv
import pathlib
import uuid
import csv
import boto3
import os
from random import randint
from fastapi import status

import pandas as pd
import pdfkit
from fpdf import FPDF
from botocore.config import Config
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import FastAPI, HTTPException,status
from typing import List
from http import HTTPStatus
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.sql import alias
from fastapi import APIRouter,Depends
from datetime import datetime, timedelta
from dotenv import load_dotenv  

from src.utils.response_utils import ResponseUtil
from src.db.models import Users, NDTnewMortgage,U_Queries
from src.utils.sso import generate_token
from src.config.constant import UserConstant
from src.config.pdf_helper import PdfHelper
from src.utils.logger_utils import LoggerUtil
from src.services.user_login1.schema import User_Schena, Query_Schema, SaveQuery, ListQuery, DeleteQuery
from src.services.user_login1.serializer import QuerySerializer, UsersSerializer,SaveSerializer,CsvSerializer,LoadSerializer,DeleteSerializer, UpdateSerializer,LogoutSerializer, SigninSerializer,SignUpSerializer

load_dotenv() # take invironment variables from .env

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

class Settings(BaseModel):
    authjwt_secret_key:str=os.getenv("AUTHJWT_SECRET_KEY")
 
@AuthJWT.load_config
def get_config():
    return Settings()

class Helper():

    @classmethod
    def loan_types_sub_convert(cls,loan_types_sub):
        loan_types_sub_convert = []
        try:
            for loan_type in loan_types_sub:
                if loan_type == "Home Equity Loan":
                    loan_types_sub = "mHMEQ"
                    loan_types_sub_convert.append(loan_types_sub)
                else:
                    loan_types_sub = "m" + loan_type
                    loan_types_sub_convert.append(loan_types_sub)
        
            return loan_types_sub_convert
        except:
            return ResponseUtil.error_response(response_code = status.HTTP_400_BAD_REQUEST,message = "somehing went wrong")

    @classmethod
    def jwt_require(cls,Authorize):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    @classmethod
    def upload_to_aws(cls,local_file, bucket, s3_file):
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)

        try:
            s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except Exception as e:
            print(e)
            return f"{e}"

    @classmethod
    def download_to_aws(cls,bucket_name,key,expiry=3600):

        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY)
        try:
            response = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket_name,'Key': key},
                                                    )
            print(response)
            return response
        except ClientError as e:
            print(e)
            return True
    
    @classmethod
    def reportheader_ary(cls,request:QuerySerializer, year = None, period = None, state = None, county = None):
        reportheader_ary = []
        created_at = str(datetime.now())
        try:
            if year and period:
                if request.usecode["usecodegroup"] == "ANY" and  request.usecode["usecode"] == "All":
                    proprty_type = "All Properties"
                elif request.usecode["usecodegroup"] == "RES" and  request.usecode["usecode"] == "All":
                    proprty_type = "All Residentials"
                elif request.usecode["usecodegroup"] == "COM" and  request.usecode["usecode"] == "All":
                    proprty_type = "All Commericals"
                else:
                    proprty_type = request.usecode["usecodegroup"] + " " + request.usecode["usecode"]
                
                if request.customregion == True:
                    if request.summarizeby == "State Level":
                        
                        if request.state[0]["state"] == "All":
                            regions = f"All Regions in All State"
                        else:
                            state = []
                            for state_value in request.state:
                                state.append(state_value["state"])
                            state_str = ' ,'.join([str(elem) for elem in state])
                            regions = f"All Regions in State of {state_str}"

                    elif request.summarizeby == "County Level":
                        if request.county[0]["county"] == "All" and request.county[0]["state"] != "All":
                            county_lst = []
                            for i in request.county:
                                county_lst.append(i["county"] + " County")
                                county_lst.append(i["state"] +" ")
                            county_str = ' ,'.join([str(elem) for elem in county_lst])
                            regions = county_str
                        elif request.county[0]["county"] == "All" and request.county[0]["state"] == "All":
                            regions = "All Regions in All County in All State"
                        else:
                            county_lst = []
                            for i in request.county:
                                county_lst.append(i["county"] + " County")
                                county_lst.append(i["state"] +" ")
                            county_str = ' ,'.join([str(elem) for elem in county_lst])
                            regions = county_str
                    ary = []
                    ary.append(proprty_type)
                    ary.append(os.getenv("PREPARED_FOR"))
                    ary.append(regions)
                    ary.append(f"{year} {period}")
                    ary.append(request.reportrank)
                    ary.append(created_at)
                    reportheader_ary.append(ary)
                else:
                    if request.summarizeby == "State Level":

                        ary = []
                        ary.append(proprty_type)
                        ary.append(os.getenv("PREPARED_FOR"))
                        ary.append(f"All Regions in State of {state}")
                        ary.append(f"{year} {period}")
                        ary.append(request.reportrank)
                        ary.append(created_at)
                        reportheader_ary.append(ary)

                    elif request.summarizeby == "County Level":
                        ary = []
                        ary.append(proprty_type)
                        ary.append(os.getenv("PREPARED_FOR"))
                        ary.append(f"All Regions in {county[0]} County, {county[1]}")
                        ary.append(f"{year} {period}")
                        ary.append(request.reportrank)
                        ary.append(created_at)
                        reportheader_ary.append(ary)
            else:
                if request.usecode["usecodegroup"] == "ANY" and  request.usecode["usecode"] == "All":
                    proprty_type = "All Properties"
                elif request.usecode["usecodegroup"] == "RES" and  request.usecode["usecode"] == "All":
                    proprty_type = "All Residentials"
                elif request.usecode["usecodegroup"] == "COM" and  request.usecode["usecode"] == "All":
                    proprty_type = "All Commericals"
                else:
                    proprty_type = request.usecode["usecodegroup"] + " " + request.usecode["usecode"]
                
                if request.customregion == True:
                    if request.summarizeby == "State Level":
                        if request.state[0]["state"] == "All":
                            regions = f"All Regions in All State"
                        else:
                            state = []
                            for state_value in request.state:
                                state.append(state_value["state"])
                            state_str = ' ,'.join([str(elem) for elem in state])
                            regions = f"All Regions in {state_str}"

                    elif request.summarizeby == "County Level":
                        if request.county[0]["state"] == "All":
                            regions = f"All County In all State"
                        else:
                            county_lst = []
                            for i in request.county:
                                county_lst.append(i["county"] + " County")
                                county_lst.append(i["state"] +" ")
                            county_str = ' ,'.join([str(elem) for elem in county_lst])
                            regions = county_str
                    ary = []
                    ary.append(proprty_type)
                    ary.append(os.getenv("PREPARED_FOR"))
                    ary.append(regions)
                    ary.append(f"{request.daterange['startdate']} / {request.daterange['enddate']}")
                    ary.append(request.reportrank)
                    ary.append(created_at)
                    reportheader_ary.append(ary)
                else:
                    if request.summarizeby == "State Level":
                        ary = []
                        ary.append(proprty_type)
                        ary.append(os.getenv("PREPARED_FOR"))
                        ary.append(f"All Regions in State of {state}")
                        ary.append(f"{request.daterange['startdate']} / {request.daterange['enddate']}")
                        ary.append(request.reportrank)
                        ary.append(created_at)
                        reportheader_ary.append(ary)

                    elif request.summarizeby == "County Level":

                        ary = []
                        ary.append(proprty_type)
                        ary.append(os.getenv("PREPARED_FOR"))
                        ary.append(f"All Regions in {county[0]} County, {county[1]}")
                        ary.append(f"{request.daterange['startdate']} / {request.daterange['enddate']}")
                        ary.append(request.reportrank)
                        ary.append(created_at)
                        reportheader_ary.append(ary)
            print(reportheader_ary)
            return reportheader_ary
        except:
            return ResponseUtil.error_response(response_code = status.HTTP_500_INTERNAL_SERVER_ERROR,message = "somehing wrong in reportheader_ary")

    
    @classmethod
    def report_ary(cls, data, pmm_data, oth_data, request:QuerySerializer):
        print("i aam here")
        print(request.brokerlenderbypass)
        print(type(request.brokerlenderbypass))
        if request.brokerlenderbypass == True:
            print(1)
        else:
            print(2)
        
        reportheader_ary = []
        report_ary = []
        internal_row_data = []
        x = 1
        t_pmm_value = 0.00
        t_pmm_count = 0
        t_oth_value = 0.00
        t_oth_count = 0
        all_value = pmm_data[0].pmm_value + oth_data[0].oth_value
        all_count = pmm_data[0].pmm_count + oth_data[0].oth_count
        for i in data:
            per_total_value = (float(i.total_value) * 100 / float(all_value) if i.total_value else 0)
            per_pmm_value = (float(i.pmm_value) * 100 / float(pmm_data[0].pmm_value) if i.pmm_value else 0)
            per_oth_value = (float(i.oth_value) * 100 / float(oth_data[0].oth_value) if i.oth_value else 0)
            if request.brokerlenderbypass == True:
                pass
            else:
                pass
            internal_row_data.append(
                [
                    f"{i.mLenderName}",
                    x, 
                    f"{randint(10,99)}",
                    f"{randint(10,99)}",
                    "${:,.2f}".format(i.total_value) if i.total_value else f"${0}",
                    f"{i.total_count}" if i.total_count else f"{0}",
                    "${:,.2f}".format(i.pmm_value) if i.pmm_value else f"${0}",
                    f"{i.pmm_count}" if i.pmm_count else f"{0}",
                    "${:,.2f}".format(i.oth_value) if i.oth_value else f"${0}",
                    f"{i.oth_count}" if i.oth_count else f"{0}",
                    f"{round(per_total_value,2)}%",
                    f"{round(per_pmm_value,2)}%",
                    f"{round(per_oth_value,2)}%"
                ]
            )
            x = x + 1
            t_pmm_value = t_pmm_value + (float(i.pmm_value) if i.pmm_value else 0.00)
            t_pmm_count = t_pmm_count + (i.pmm_count if i.pmm_count else 0)
            t_oth_value = t_oth_value + (float(i.oth_value) if i.oth_value else 0.00)
            t_oth_count = t_oth_count + (i.oth_count if i.oth_count else 0)

        
        remaining_value = float(all_value) - (t_pmm_value + t_oth_value)
        remaining_pmm_value = float(pmm_data[0].pmm_value) - t_pmm_value
        remaining_oth_value = float(oth_data[0].oth_value) - t_oth_value
        remaining_count = all_count - (t_pmm_count + t_oth_count)
        remaining_per_total_value = float(remaining_value) * 100 / float(all_value)
        remaining_per_pmm_value = float(remaining_pmm_value) * 100 / float(pmm_data[0].pmm_value)
        remaining_per_oth_value = float(remaining_oth_value) * 100 / float(oth_data[0].oth_value)
        
        internal_row_data.append(
            [
                "(All Other Lenders)",
                '',
                '',
                '',
                "${:,.2f}".format(remaining_value) if remaining_value else f"${0}",
                f"{remaining_count}" if remaining_count else f"0",
                "${:,.2f}".format(remaining_pmm_value) if t_pmm_value else f"${0}",
                f"{t_pmm_count}" if t_pmm_count else f"0",
                "${:,.2f}".format(remaining_oth_value) if t_oth_value else f"${0}",
                f"{t_oth_count}" if t_oth_count else f"0",
                f"{round(remaining_per_total_value,2)}%",
                f"{round(remaining_per_pmm_value,2)}%",
                f"{round(remaining_per_oth_value,2)}%"
            ]
        )
        
        
        internal_row_data.append(
            [
                "All",
                '',
                '',
                '',
                "${:,.2f}".format(all_value) if all_value else f"${0}",
                f"{all_count}" if all_count else f"0",
                "${:,.2f}".format(pmm_data[0].pmm_value) if pmm_data[0].pmm_value else f"${0}",
                f"{pmm_data[0].pmm_count}" if pmm_data[0].pmm_count else f"0",
                "${:,.2f}".format(oth_data[0].oth_value) if oth_data[0].oth_value else f"${0}",
                f"{oth_data[0].oth_count}" if oth_data[0].oth_count else f"0",
                "100%",
                "100%",
                "100%"
            ]
        )
        report_ary.append(internal_row_data)
        
        return report_ary

##### MARKET SHARE MODULE (login, run_query, save_query, load_query) #####

class Users_Module():
    @classmethod
    async def signup(cls,request:SignUpSerializer,Authorize,db):

        user = User_Schena.user_signup(request,db)
        data = {}
        access_token=Authorize.create_access_token(subject=user.usr_id,expires_time = timedelta(minutes=1440))
        refresh_token=Authorize.create_refresh_token(subject=user.usr_id,expires_time = timedelta(minutes=1440))
        data["sso_token"] = user.usr_sso
        data["access_token"] = access_token
        data["refresh_token"]= refresh_token
        return ResponseUtil.success_response(data,message=UserConstant.LOGIN_SUCCESS)
    
    @classmethod
    async def signin(cls,request:SigninSerializer,Authorize,db):

        user = User_Schena.user_signin(request,db)
        
        if user:
            data = {}
            access_token=Authorize.create_access_token(subject=user.usr_id,expires_time = timedelta(minutes=1440))
            refresh_token=Authorize.create_refresh_token(subject=user.usr_id,expires_time = timedelta(minutes=1440))
            data["sso_token"] = user.usr_sso
            data["access_token"] = access_token
            data["refresh_token"]= refresh_token
            return ResponseUtil.success_response(data,message=UserConstant.LOGIN_SUCCESS)
        else:
            return ResponseUtil.error_response(message = "User not Found")

    @classmethod
    async def login(cls,request:UsersSerializer,Authorize,db):
        try:
            user = User_Schena.user_login(request.usr_email,db)
        except Exception as e:
            LoggerUtil.error(UserConstant.ERROR_MESSAGE)
            return ResponseUtil.error_response(message = UserConstant.ERROR_MESSAGE)

        try:
            if user != None:
                LoggerUtil.info(UserConstant.USER_GET)
                if (user.usr_username==request.usr_username) and (user.usr_password==request.usr_password):
                    access_token=Authorize.create_access_token(subject=user.usr_id,expires_time = timedelta(minutes=1440))
                    refresh_token=Authorize.create_refresh_token(subject=user.usr_id,expires_time = timedelta(minutes=1440))
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
        # Helper.jwt_require(Authorize=Authorize)

        reportheader_ary = []
        report_ary = []
        try:
            if (len(request.year) > 0 and len(request.period) > 0) or request.isdaterange:
                pmm_data, oth_data = Query_Schema.get_all_data(db)
                if request.isdaterange:
                    if request.customregion:
                        LoggerUtil.info(UserConstant.COUNTY_STATE)
                        data = Query_Schema.master_query(db, request)
                        reportheader_ary.extend(Helper.reportheader_ary(request))
                        report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data, request=request))
                    else:
                        LoggerUtil.info(UserConstant.GET_STATE)
                        if request.summarizeby == "State Level":
                            if request.state[0]["state"] == "All":
                                LoggerUtil.info(UserConstant.GET_STATE_P)
                                state_distinct_data = Query_Schema.state_data(db)
                                state_data = []
                                for each in state_distinct_data:
                                    state_data.append(each[0])
                            else:
                                LoggerUtil.info(UserConstant.GET_STATE_ONLY)
                                state_data = []
                                for each in request.state:
                                    state_data.append(each["state"])                
                            for state in state_data:
                                data = Query_Schema.master_query(db, request,state=state)
                                LoggerUtil.info(UserConstant.STATE_REPORTHEADER)
                                reportheader_ary.extend(Helper.reportheader_ary(request,state=state))
                                LoggerUtil.info(UserConstant.STATE_REPORT_ARY)
                                report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data, request=request))

                            LoggerUtil.info(UserConstant.GET_COUNTY)
                        elif request.summarizeby == "County Level":
                            LoggerUtil.info(UserConstant.COUNTY_STATE)
                            if request.county[0]["county"] == "All" and request.county[0]["state"] != "All":
                                state_data = []
                                for each in request.county:
                                    state_data.append(each["state"])
                                county_data = Query_Schema.county_data(db,county_data=state_data)
                                LoggerUtil.info(UserConstant.GET_STATE_P)
                            elif request.county[0]["county"] == "All" and request.county[0]["state"] == "All":
                                state_distinct_data = Query_Schema.state_data(db)
                                state_data = []
                                for each in state_distinct_data:
                                    state_data.append(each[0])
                                    LoggerUtil.info(UserConstant.GET_STATE_P)
                                county_data = Query_Schema.county_data(db,county_data=state_data)
                            else:
                                LoggerUtil.info(UserConstant.COUNTY_STATE)    
                                county_data = []
                                for each in request.county:
                                    county_data.append([each["county"], each["state"]])
                                LoggerUtil.info(UserConstant.COUNTY_STATE)
                            for county in county_data:
                                data = Query_Schema.master_query(db, request,county=county)
                                reportheader_ary.extend(Helper.reportheader_ary(request,county=county))
                                report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data, request=request))

                else:
                    LoggerUtil.info(UserConstant.YEAR_PERIOD)
                    year_data = request.year
                    period_data = request.period
                    if request.customregion:
                        for year in year_data:
                            for period in period_data:
                                data = Query_Schema.master_query(db, request, year, period)
                                reportheader_ary.extend(Helper.reportheader_ary(request, year=year, period=period))
                                report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data, request=request))
                    else:
                        LoggerUtil.info(UserConstant.COUNTY_STATE)
                        if request.summarizeby == "State Level":
                            if request.state[0]["state"] == "All":
                                state_distinct_data = Query_Schema.state_data(db)
                                state_data = []
                                for each in state_distinct_data:
                                    state_data.append(each[0])
                            else:
                                LoggerUtil.info(UserConstant.COUNTY_STATE)
                                state_data = []
                                for each in request.state:
                                    state_data.append(each["state"])
                                
                                LoggerUtil.info(UserConstant.YEAR_PERIOD_STATE)
                            for state in state_data:
                                for year in year_data:
                                    for period in period_data:
                                        data = Query_Schema.master_query(db, request, year, period, state=state)
                                        reportheader_ary.extend(Helper.reportheader_ary(request, year=year, period=period, state=state))
                                        LoggerUtil.info(UserConstant.COUNTY_STATE)
                                        report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data, request=request))

                            LoggerUtil.info(UserConstant.GET_COUNTY)
                        elif request.summarizeby == "County Level":
                            LoggerUtil.info(UserConstant.COUNTY_STATE)
                            if request.county[0]["county"] == "All" and request.county[0]["state"] != "All":
                                print("i am here in all county pr state")
                                state_data = []
                                for each in request.county:
                                    state_data.append(each["state"])
                                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                                county_data = Query_Schema.county_data(db,county_data=state_data)
                                LoggerUtil.info(UserConstant.COUNTY_STATE)
                            elif request.county[0]["county"] == "All" and request.county[0]["state"] == "All":
                                print("i am here in all county All state")
                                state_distinct_data = Query_Schema.state_data(db)
                                state_data = []
                                for each in state_distinct_data:
                                    state_data.append(each[0])
                                print("All state in all county :- ",state_data)
                                print("len of state :- ",len(state_data))
                                county_data = Query_Schema.county_data(db,county_data=state_data)
                                print("all county data and all state :- ", county_data)
                                print("len of all county data and all state :- ", len(county_data))
                            else:
                                LoggerUtil.info(UserConstant.COUNTY_STATE)    
                                county_data = []
                                for each in request.county:
                                    county_data.append([each["county"], each["state"]])
                                    LoggerUtil.info(UserConstant.YEAR_PERIOD_COUNTY)
                            for county in county_data:
                                for year in year_data:
                                    for period in period_data:
                                        data = Query_Schema.master_query(db, request, year, period, county=county)
                                        reportheader_ary.extend(Helper.reportheader_ary(request, year=year, period=period, county=county))
                                        report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data, request=request))
        except:
            LoggerUtil.error("Internl server error")
            return ResponseUtil.error_response(response_code = status.HTTP_500_INTERNAL_SERVER_ERROR,message = "Internl server error")

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
        final_data["report_ary"] = report_ary
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
    async def saveq(cls,request:SaveSerializer,db):
        save_query = SaveQuery.save_query(request,db)
        try:
            final_data = {}
            final_data["q_id"] = save_query.q_id
            LoggerUtil.info(UserConstant.SAVEQ)
            return ResponseUtil.success_response(final_data,message="Success")
        except:
            return ResponseUtil.error_response(response_code = status.HTTP_422_UNPROCESSABLE_ENTITY,message = "dont save data")
        
    @classmethod
    async def updateq(cls,request:UpdateSerializer,db):
        try:
            update_query = SaveQuery.update_query(request,db)
            final_data = {}
            final_data["q_id"] = request.q_id
            final_data["usr_id"] = request.usr_id
            final_data["q_name"] = request.q_name

            LoggerUtil.info(UserConstant.UPDATEQ)
            return ResponseUtil.success_response(final_data,message="Success")
        except:
            return ResponseUtil.error_response(response_code = status.HTTP_400_BAD_REQUEST,message = "dont update data")
    
    @classmethod
    # async def logoutq(token: str = Depends(login.access_token)):
    #     expires(0,token)
    #     return {"response": "Logged out"}
    async def logoutq(cls,request:LogoutSerializer,db):
        try:
            final_data = {}
            final_data["message"] = "Logout succesfully"
            LoggerUtil.info(UserConstant.LOGOUTQ)
            return ResponseUtil.success_response(final_data,message="Success")
        except:
            return ResponseUtil.error_response(response_code = status.HTTP_500_INTERNAL_SERVER_ERROR,message = "internal server error")

    
    @classmethod
    async def listq(cls,request:LoadSerializer,db):
        liste_query = ListQuery.list_query(request,db)
        final_list_data = []
        try:
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

            LoggerUtil.info(UserConstant.LISTQ)
            return ResponseUtil.success_response(final_data,message="Success")
        except:
            return ResponseUtil.error_response(response_code = status.HTTP_404_NOT_FOUND,message = "list is not found")

    @classmethod
    async def deleteq(cls,request:DeleteSerializer,db):
        delete_query = DeleteQuery.delete_query(request,db)
        try:
            final_data = {}
            final_data["q_id"] = request.q_id
            final_data["usr_id"] = request.usr_id
            final_data["countaffected"] = 1
            LoggerUtil.info(UserConstant.DELETEQ)
            return ResponseUtil.success_response(final_data,message="Success")
        except:
            return ResponseUtil.error_response(response_code = status.HTTP_400_BAD_REQUEST,message = "bad request")

    @classmethod
    async def csv(cls,request:CsvSerializer):
        
        LoggerUtil.info(UserConstant.CSV_REPORT)
        cur_report_header_ary = request.cur_report_header_ary
        first_header =[ f"{cur_report_header_ary[0][0]}  Mortgage Marketshare Report. Prepared for: {cur_report_header_ary[0][1]}"]
        
        LoggerUtil.info(UserConstant.CSV_ARY)
        cur_report_ary = request.cur_report_ary
        subtitle = ["Lender Name","All","P","N","Total Value","Total Number","Total Value","Total Number","Total Value","Total Number","All","P","NP"]

        file_name = uuid.uuid4()
        current_path = pathlib.Path().absolute()
        path = f'{current_path}/src/files'
        print(current_path)
        with open(f'{path}/{file_name}.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(first_header)

            for i in range (len(cur_report_header_ary)):
                header = [f"Rank by {cur_report_header_ary[i][4]}","","","","All Mortgages","","Purchase Mortgages","","Non Purchase Mortgages","",f"Mkt Shr by {cur_report_header_ary[i][4]}"]
                writer.writerow([cur_report_header_ary[i][2]])
                writer.writerow([cur_report_header_ary[i][3]])
                writer.writerow(header)
                writer.writerow(subtitle)
                try:
                    writer.writerows(cur_report_ary[i])
                    writer.writerow(" ")
                    writer.writerow(" ")
                except:
                    writer.writerow(" ")
                    writer.writerow(" ")
                    pass

        Helper.upload_to_aws(local_file=f'{path}/{file_name}.csv',bucket="loanapp-s3",s3_file=f'{file_name}.csv')

        url = Helper.download_to_aws(bucket_name="loanapp-s3",key = f'{file_name}.csv')

        url = (url.split("?")[0])

        LoggerUtil.info(UserConstant.CSV)
        return ResponseUtil.success_response(url,message="Success")

    @classmethod
    async def txt(cls,request:CsvSerializer):
        
        LoggerUtil.info(UserConstant.TXT_REPORT)
        cur_report_header_ary = request.cur_report_header_ary
        first_header =[ f"{cur_report_header_ary[0][0]}  Mortgage Marketshare Report. Prepared for: {cur_report_header_ary[0][1]}"]
        
        LoggerUtil.info(UserConstant.TXT_ARY)
        cur_report_ary = request.cur_report_ary
        subtitle = ["Lender Name\t","All\t","P\t","N\t","Total Value\t","Total Number\t","Total Value\t","Total Number\t","Total Value\t","Total Number\t","All\t","P\t","NP\t"]

        file_name = uuid.uuid4()
        current_path = pathlib.Path().absolute()
        path = f'{current_path}/src/files'
        print(current_path)
        with open(f'{path}/{file_name}.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(first_header)

            for i in range (len(cur_report_header_ary)):
                header = [f"Rank by {cur_report_header_ary[i][4]}\t\t\t","All Mortgages\t\t","Purchase Mortgages\t\t","Non Purchase Mortgages\t\t",f"Mkt Shr by {cur_report_header_ary[i][4]}"]
                writer.writerow([cur_report_header_ary[i][2]])
                writer.writerow([cur_report_header_ary[i][3]])
                writer.writerow(header)
                writer.writerow(subtitle)
                try:
                    for row_lst in cur_report_ary[i]:
                        for j in range(len(row_lst)):
                            row_lst[j] = str(row_lst[j]) + "\t"
                            if str(row_lst[j][0]) == "$":
                                row_lst[j] = row_lst[j].replace(',',':')
                    writer.writerows(cur_report_ary[i])
                    writer.writerow(" ")
                    writer.writerow(" ")
                except:
                    writer.writerow(" ")
                    writer.writerow(" ")
                    pass

        with open(f'{path}/{file_name}.csv', 'r') as f_in, open(f'{path}/{file_name}.txt', 'w') as f_out:
            content = f_in.read().replace(',', ' ')
            content = content.replace(':', ',')
            f_out.write(content)
        Helper.upload_to_aws(local_file=f'{path}/{file_name}.txt',bucket="loanapp-s3",s3_file=f'{file_name}.txt')
        
        url = Helper.download_to_aws(bucket_name="loanapp-s3",key = f'{file_name}.txt')
        url = (url.split("?")[0])
        LoggerUtil.info(UserConstant.TXT)
        return ResponseUtil.success_response(url,message="Success")

    @classmethod
    async def xls(cls,request:CsvSerializer):
        
        LoggerUtil.info(UserConstant.XLS_REPORT)
        cur_report_header_ary = request.cur_report_header_ary
        first_header =[ f"{cur_report_header_ary[0][0]}  Mortgage Marketshare Report. Prepared for: {cur_report_header_ary[0][1]}"]

        LoggerUtil.info(UserConstant.XLS_ARY)
        cur_report_ary = request.cur_report_ary
        subtitle = ["Lender Name","All","P","N","Total Value","Total Number","Total Value","Total Number","Total Value","Total Number","All","P","NP"]

        file_name = uuid.uuid4()
        current_path = pathlib.Path().absolute()
        path = f'{current_path}/src/files'
        print(current_path)
        with open(f'{path}/{file_name}.xls', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(first_header)

            for i in range (len(cur_report_header_ary)):
                header = [f"Rank by {cur_report_header_ary[i][4]}","","","","All Mortgages","","Purchase Mortgages","","Non Purchase Mortgages","",f"Mkt Shr by {cur_report_header_ary[i][4]}"]
                writer.writerow([cur_report_header_ary[i][2]])
                writer.writerow([cur_report_header_ary[i][3]])
                writer.writerow(header)
                writer.writerow(subtitle)
                try:
                    writer.writerows(cur_report_ary[i])
                    writer.writerow(" ")
                    writer.writerow(" ")
                except:
                    writer.writerow(" ")
                    writer.writerow(" ")
                    pass

        Helper.upload_to_aws(local_file=f'{path}/{file_name}.xls',bucket="loanapp-s3",s3_file=f'{file_name}.xls')

        url = Helper.download_to_aws(bucket_name="loanapp-s3",key = f'{file_name}.xls')
        url = (url.split("?")[0])

        LoggerUtil.info(UserConstant.XLS)
        return ResponseUtil.success_response(url,message="Success")
 
            
    @classmethod
    async def pdf(cls,request:CsvSerializer):

        html_string = PdfHelper.html_create(request)
        current_path = pathlib.Path().absolute()
        path = f'{current_path}/src/files'
        file_name = uuid.uuid4()
        options = {'page-size':'A3'}
        pdfkit.from_string((html_string),f'{path}/{file_name}.pdf',options=options)


       
        url = Helper.download_to_aws(bucket_name="loanapp-s3",key = f'{file_name}.pdf')
        url = (url.split("?")[0])

        LoggerUtil.info(UserConstant.PDF)
        return ResponseUtil.success_response(url,message="Success")
    
