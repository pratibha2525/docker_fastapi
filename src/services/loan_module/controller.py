from fastapi import FastAPI, HTTPException,status
from typing import List
from http import HTTPStatus
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.sql import alias
from datetime import datetime, timedelta
from random import randint

from src.services.loan_module.serializer import Lo_UsersSerializer, QuerySerializer, SaveSerializer, UpdateSerializer,DeleteSerializer,LoadSerializer,CsvSerializer
from src.services.loan_module.schema import User_Schema, SaveQuery, DeleteQuery, ListQuery, Query_Schema
from src.utils.response_utils import ResponseUtil
from src.config.constant import UserConstant
from src.utils.logger_utils import LoggerUtil
from datetime import datetime, timedelta


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

    @classmethod
    def jwt_require(cls,Authorize):
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    # @classmethod
    # def upload_to_aws(cls,local_file, bucket, s3_file):
    #     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
    #                     aws_secret_access_key=SECRET_KEY)

    #     try:
    #         s3.upload_file(local_file, bucket, s3_file)
    #         print("Upload Successful")
    #         return True
    #     except FileNotFoundError:
    #         print("The file was not found")
    #         return False
    #     except Exception as e:
    #         print(e)
    #         return f"{e}"

    # @classmethod
    # def download_to_aws(cls,bucket_name,key,expiry=3600):

    #     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
    #                         aws_secret_access_key=SECRET_KEY)
    #     try:
    #         response = s3.generate_presigned_url('get_object',
    #                                         Params={'Bucket': bucket_name,'Key': key},
    #                                                 )
    #         print(response)
    #         return response
    #     except ClientError as e:
    #         print(e)
    #         return True
    
    @classmethod
    def reportheader_ary(cls,request:QuerySerializer, year = None, period = None, state = None, county = None):
        reportheader_ary = []
        created_at = str(datetime.now())
        if year and period:
            if request.usecode["usecodegroup"] == "ANY" and  request.usecode["usecode"] == "All":
                proprty_type = "All Properties"
            elif request.usecode["usecodegroup"] == "RES" and  request.usecode["usecode"] == "All":
                proprty_type = "All Residentials"
            # elif request.usecode["usecodegroup"] == "COM" and  request.usecode["usecode"] == "All":
            #     proprty_type = "All Commericals"
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
                ary.append("Skyward Techno.")
                ary.append(regions)
                ary.append(f"{year} {period}")
                ary.append(request.reportrank)
                ary.append(created_at)
                reportheader_ary.append(ary)
            else:
                if request.summarizeby == "State Level":

                    ary = []
                    ary.append(proprty_type)
                    ary.append("Skyward Techno.")
                    ary.append(f"All Regions in State of {state}")
                    ary.append(f"{year} {period}")
                    ary.append(request.reportrank)
                    ary.append(created_at)
                    reportheader_ary.append(ary)

                elif request.summarizeby == "County Level":
                    ary = []
                    ary.append(proprty_type)
                    ary.append("Skyward Techno.")
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
            # elif request.usecode["usecodegroup"] == "COM" and  request.usecode["usecode"] == "All":
            #     proprty_type = "All Commericals"
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
                ary.append("Skyward Techno.")
                ary.append(regions)
                ary.append(f"{request.daterange['startdate']} / {request.daterange['enddate']}")
                ary.append(request.reportrank)
                ary.append(created_at)
                reportheader_ary.append(ary)
            else:
                if request.summarizeby == "State Level":
                    ary = []
                    ary.append(proprty_type)
                    ary.append("Skyward Techno.")
                    ary.append(f"All Regions in State of {state}")
                    ary.append(f"{request.daterange['startdate']} / {request.daterange['enddate']}")
                    ary.append(request.reportrank)
                    ary.append(created_at)
                    reportheader_ary.append(ary)

                elif request.summarizeby == "County Level":

                    ary = []
                    ary.append(proprty_type)
                    ary.append("Skyward Techno.")
                    ary.append(f"All Regions in {county[0]} County, {county[1]}")
                    ary.append(f"{request.daterange['startdate']} / {request.daterange['enddate']}")
                    ary.append(request.reportrank)
                    ary.append(created_at)
                    reportheader_ary.append(ary)
        print(reportheader_ary)
        return reportheader_ary
    
    @classmethod
    def report_ary(cls, data, pmm_data, oth_data):
        reportheader_ary = []
        report_ary = []
        internal_row_data = []
        x = 1
        # t_pmm_value = 0.00
        # t_pmm_count = 0
        # t_oth_value = 0.00
        # t_oth_count = 0
        # all_value = pmm_data[0].pmm_value + oth_data[0].oth_value
        # all_count = pmm_data[0].pmm_count + oth_data[0].oth_count
        for i in data:
            print("\t\t\t\t\t\n\n\n",i)
            print(i.num_loans)
            print(i.total_amount,"\n\n")
            all_total_amount = int(f"{i.total_amount}" if i.total_amount else f"{0}") + int(f"{i.x_amt}"if i.x_amt else f"{0}")
            all_num_loans = int(f"{i.num_loans}"if i.num_loans else f"{0}") + int(f"{i.x_num}"if i.x_num else f"{0}")
            # per_total_value = (float(i.total_value) * 100 / float(all_value) if i.total_value else 0)
            # per_pmm_value = (float(i.pmm_value) * 100 / float(pmm_data[0].pmm_value) if i.pmm_value else 0)
            # per_oth_value = (float(i.oth_value) * 100 / float(oth_data[0].oth_value) if i.oth_value else 0)
            internal_row_data.append(
                [
                    x, 
                    f"{i.mOrigName}",
                    f"{i.mOrigID}",
                    f"{i.mLenderName}",
                    f"${all_total_amount}",
                    f"{all_num_loans}",
                    f"${i.total_amount}" if i.total_amount else f"${0}",
                    f"{i.num_loans}"if i.num_loans else f"{0}",
                    f"${i.x_amt}"if i.x_amt else f"${0}",
                    f"{i.x_num}"if i.x_num else f"{0}",
                    # f"${i.total_value}" if i.total_value else f"${0}",
                    # f"{i.total_count}" if i.total_count else f"{0}",
                    # f"${i.pmm_value}" if i.pmm_value else f"${0}",
                    # f"{i.pmm_count}" if i.pmm_count else f"{0}",
                    # f"${i.oth_value}" if i.oth_value else f"${0}",
                    # f"{i.oth_count}" if i.oth_count else f"{0}",
                ]
            )
            x = x + 1
            # t_pmm_value = t_pmm_value + (float(i.pmm_value) if i.pmm_value else 0.00)
            # t_pmm_count = t_pmm_count + (i.pmm_count if i.pmm_count else 0)
            # t_oth_value = t_oth_value + (float(i.oth_value) if i.oth_value else 0.00)
            # t_oth_count = t_oth_count + (i.oth_count if i.oth_count else 0)

        
        # remaining_value = float(all_value) - (t_pmm_value + t_oth_value)
        # remaining_pmm_value = float(pmm_data[0].pmm_value) - t_pmm_value
        # remaining_oth_value = float(oth_data[0].oth_value) - t_oth_value
        # remaining_count = all_count - (t_pmm_count + t_oth_count)
        # remaining_per_total_value = float(remaining_value) * 100 / float(all_value)
        # remaining_per_pmm_value = float(remaining_pmm_value) * 100 / float(pmm_data[0].pmm_value)
        # remaining_per_oth_value = float(remaining_oth_value) * 100 / float(oth_data[0].oth_value)
        
        # internal_row_data.append(
        #     [
        #         "(All Other Lenders)",
        #         '',
        #         '',
        #         '',
        #         f"${remaining_value}" if remaining_value else f"${0}",
        #         f"{remaining_count}" if remaining_count else f"0",
        #         f"${remaining_pmm_value}" if t_pmm_value else f"${0}",
        #         f"{t_pmm_count}" if t_pmm_count else f"0",
        #         f"${remaining_oth_value}" if t_oth_value else f"${0}",
        #         f"{t_oth_count}" if t_oth_count else f"0",
        #         f"{round(remaining_per_total_value,2)}%",
        #         f"{round(remaining_per_pmm_value,2)}%",
        #         f"{round(remaining_per_oth_value,2)}%"
        #     ]
        # )
        
        
        # internal_row_data.append(
        #     [
        #         "All",
        #         '',
        #         '',
        #         '',
        #         f"${all_value}" if all_value else f"${0}",
        #         f"{all_count}" if all_count else f"0",
        #         f"${pmm_data[0].pmm_value}" if pmm_data[0].pmm_value else f"${0}",
        #         f"{pmm_data[0].pmm_count}" if pmm_data[0].pmm_count else f"0",
        #         f"${oth_data[0].oth_value}" if oth_data[0].oth_value else f"${0}",
        #         f"{oth_data[0].oth_count}" if oth_data[0].oth_count else f"0",
        #         "100%",
        #         "100%",
        #         "100%"
        #     ]
        # )
        report_ary.append(internal_row_data)
        
        return report_ary

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
    async def query(cls, request:QuerySerializer,db):
        reportheader_ary = []
        report_ary = []
        # pmm_data, oth_data = Query_Schema.get_all_data(db)
        # data = Query_Schema.master_query(db, request)
            

        if (len(request.year) > 0 and len(request.period) > 0) or request.isdaterange:
            pmm_data, oth_data = Query_Schema.get_all_data(db)
            if request.isdaterange:
                if request.customregion:
                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                    data = Query_Schema.master_query(db, request)
                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                    reportheader_ary.extend(Helper.reportheader_ary(request))
                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                    report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data))
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
                            report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data))

                        LoggerUtil.info(UserConstant.GET_COUNTY)
                    elif request.summarizeby == "County Level":
                        LoggerUtil.info(UserConstant.COUNTY_STATE)
                        if request.county[0]["county"] == "All" and request.county[0]["state"] != "All":
                            state_data = []
                            for each in request.county:
                                state_data.append(each["state"])
                            LoggerUtil.info(UserConstant.COUNTY_STATE)
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
                            report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data))

            else:
                year_data = request.year
                period_data = request.period
                if request.customregion:
                    for year in year_data:
                        for period in period_data:
                            data = Query_Schema.master_query(db, request, year, period)
                            LoggerUtil.info(UserConstant.COUNTY_STATE)
                            reportheader_ary.extend(Helper.reportheader_ary(request, year=year, period=period))
                            LoggerUtil.info(UserConstant.COUNTY_STATE)
                            report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data))
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
                            
                            LoggerUtil.info(UserConstant.COUNTY_STATE)
                        for state in state_data:
                            for year in year_data:
                                for period in period_data:
                                    data = Query_Schema.master_query(db, request, year, period, state=state)
                                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                                    reportheader_ary.extend(Helper.reportheader_ary(request, year=year, period=period, state=state))
                                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                                    report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data))

                        LoggerUtil.info(UserConstant.COUNTY_STATE)
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
                                LoggerUtil.info(UserConstant.COUNTY_STATE)
                            county_data = Query_Schema.county_data(db,county_data=state_data)
                        else:
                            LoggerUtil.info(UserConstant.COUNTY_STATE)    
                            county_data = []
                            for each in request.county:
                                county_data.append([each["county"], each["state"]])
                                LoggerUtil.info(UserConstant.COUNTY_STATE)
                        for county in county_data:
                            for year in year_data:
                                for period in period_data:
                                    data = Query_Schema.master_query(db, request, year, period, county=county)
                                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                                    reportheader_ary.extend(Helper.reportheader_ary(request, year=year, period=period, county=county))
                                    LoggerUtil.info(UserConstant.COUNTY_STATE)
                                    report_ary.extend(Helper.report_ary(data=data, pmm_data=pmm_data, oth_data=oth_data))

        subheader = ["Total","Purchase Mortgages","Non Purchase Mortgages"]
        subtitle = ["Rank","Loan Originator Name","NMLS #","Authorized to Represent","Amount","#","Amount","#","Amount","#"]



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
        final_data['uid'] = ""
        final_data['tmp_inner'] = ""
        final_data['ifilter'] = ""
        final_data['report_ary'] = report_ary
        final_data['reportheader_ary'] = reportheader_ary
        final_data['reportfull_ary'] = ""
        final_data['sql'] = ""
        final_data['tsql'] = ""
        final_data['report'] = ""
        final_data["subheader"] = subheader
        final_data["subtitle"] = subtitle
        
        return final_data

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
