from sqlalchemy import or_
from src.db.database import get_db
from src.db.models import Users, NDTnewMortgage,U_Queries
from src.services.user_login1.serializer import UsersSerializer, QuerySerializer, SaveSerializer, LoadSerializer, DeleteSerializer, UpdateSerializer,LogoutSerializer, SignUpSerializer, SigninSerializer
from sqlalchemy import func
import sqlalchemy
import uuid

class User_Schena():

    @classmethod
    def user_login(cls,usr_email,db):
        data = db.query(
            Users
        ).filter(
            Users.usr_email==usr_email
        ).first()

        return data
    
    @classmethod
    def user_signin(cls,request:SigninSerializer,db):

        data = db.query(
            Users
        ).filter(
            Users.usr_email == request.usr_email,
        ).first()
        
        return data
    
    @classmethod
    def user_signup(cls,request:SignUpSerializer,db):
        sso_token = str(uuid.uuid4())
        data = Users(
            usr_username = request.usr_username,
            usr_email = request.usr_email,
            usr_password = request.usr_password,
            usr_sso = sso_token
        )
        db.add(data)
        db.commit()
        
        usr_data = db.query(
            Users
        ).filter(
            Users.usr_sso == sso_token
        ).first()
        return usr_data

class Query_Schema():
    
    @classmethod
    def state_data(cls,db):
        data = db.query(
            NDTnewMortgage.mState
        ).distinct().all()
        
        return data
    
    @classmethod
    def county_data(cls,db,county_data):
        data = db.query(
            NDTnewMortgage.mCounty,
            NDTnewMortgage.mState
        ).filter(
            NDTnewMortgage.mState.in_(county_data)
        ).distinct().all()
        
        return data

    @classmethod
    def master_query(cls, db, request:QuerySerializer, year = None, period = None, state = None, county = None):
        pmm_data = db.query(
            NDTnewMortgage.mLenderName,
            func.sum(NDTnewMortgage.mAmount).label("pmm_value"),
            func.count(NDTnewMortgage.mLenderName).label("pmm_count")
        ).filter(
            NDTnewMortgage.mLoanUse == "PMM",
            NDTnewMortgage.mLenderName.not_ilike('Miscellaneous%')
        ).group_by(NDTnewMortgage.mLenderName).subquery()
        
        oth_data = db.query(
            NDTnewMortgage.mLenderName,
            func.sum(NDTnewMortgage.mAmount).label("oth_value"),
            func.count(NDTnewMortgage.mLenderName).label("oth_count")
        ).filter(
            NDTnewMortgage.mLoanUse == "OTH",
            NDTnewMortgage.mLenderName.not_ilike('Miscellaneous%')
        ).group_by(NDTnewMortgage.mLenderName).subquery()

        data = db.query(
            NDTnewMortgage.mLenderName,
            func.sum(NDTnewMortgage.mAmount).label("total_value"),
            func.count(NDTnewMortgage.mLenderName).label("total_count"),
            pmm_data,
            oth_data
        ).outerjoin(
            pmm_data,
            pmm_data.c.mLenderName == NDTnewMortgage.mLenderName
        ).outerjoin(
            oth_data,
            oth_data.c.mLenderName == NDTnewMortgage.mLenderName
        ).group_by(NDTnewMortgage.mLenderName,pmm_data,oth_data)

        if request.reportrank == "# Loans":
            print(f"Report Rank: Loans")
            data = data.order_by(func.count(NDTnewMortgage.mLenderName).desc())
        elif request.reportrank == "$ Volume":
            print(f"Report Rank: Volumes")
            data = data.order_by(func.sum(NDTnewMortgage.mAmount).desc())

        print(f"Loan Purpose : {request.loanpurpose}")
        if request.loanpurpose == "Purchase":
            data = data.filter(
                NDTnewMortgage.mLoanUse == "PMM"
            ).order_by(func.sum(NDTnewMortgage.mAmount).desc())
        elif request.loanpurpose == "Non-Purchase":
            data = data.filter(
                NDTnewMortgage.mLoanUse == "OTH"
            ).order_by(func.sum(NDTnewMortgage.mAmount).desc())

        if request.usecode:
            print(f"Usecode {request.usecode}")
            if  request.usecode["usecodegroup"] == "RES" and  request.usecode["usecode"] == "All":
                data = data.filter(
                    NDTnewMortgage.mPropType == request.usecode["usecodegroup"]
                )
            elif  request.usecode["usecodegroup"] == "COM" and  request.usecode["usecode"] == "All":
                data = data.filter(
                    NDTnewMortgage.mPropType == request.usecode["usecodegroup"]
                    )
            elif request.usecode["usecodegroup"] == "ANY" and  request.usecode["usecode"] == "All":
                data = data
            else:
                usecode = request.usecode["usecode"].upper()
                data = data.filter(
                    NDTnewMortgage.mPropType == request.usecode["usecodegroup"],
                    NDTnewMortgage.mPropSubTP == usecode 
                )
                
        if request.lendertype:
            if request.lendertype == "Any":
                data = data
            else:
                data =  data.filter(
                    NDTnewMortgage.mLenderType == request.lendertype
                )
                
        if request.lenders:
            data = data.filter(
                NDTnewMortgage.mLenderName.in_(request.lenders)
            )
        
        if request.loantypes:
            if request.loantypes == "All":
                data = data
            elif request.loantypes == "Conforming":
                data =  data.filter(
                    NDTnewMortgage.mCONFORMING == "T"
                )
            elif request.loantypes == "Jumbo":
                data =  data.filter(
                    NDTnewMortgage.mJUMBO == "T"
                )

        if request.loantypessub:
            if "ARM" in request.loantypessub:
                data = data.filter(
                    NDTnewMortgage.mARM == "T"
                )

            if "FHA" in request.loantypessub:
                data = data.filter(
                    NDTnewMortgage.mFHA == "T"
                )

            if "Home Equity Loan" in request.loantypessub:
                data = data.filter(
                    NDTnewMortgage.mHMEQ == "T"
                )

            if "HELOC" in request.loantypessub:
                data = data.filter(
                    NDTnewMortgage.mHELOC == "T"
                )

            if "Reverse" in request.loantypessub:
                data = data.filter(
                    NDTnewMortgage.mReverse == "T"
                )

            if "VHA" in request.loantypessub:
                data = data.filter(
                    NDTnewMortgage.mFHA == "T"
                )
        
        if request.refionly:
            if request.refionly == True:
                data = data.filter(
                    NDTnewMortgage.mHMEQ == "F",
                    NDTnewMortgage.mHELOC == "F"
                )
        
        if request.excl_usahud:
            if request.excl_usahud == True:
                data = data.filter(
                    NDTnewMortgage.mLenderName != "USA Housing and Urban Development",
                    NDTnewMortgage.mLenderName != "DEPARTMENT OF HOUSING & URBAN DEV"
                )

        if request.loantypessubbypass:
            if request.loantypessubbypass == True:
                data = data.filter(
                        NDTnewMortgage.mHELOC == "T",
                        NDTnewMortgage.mHMEQ == "T",
                        )
        
        if request.customregion:
            if request.summarizeby == "State Level":
                state_data = []
                if request.state[0]["state"] == "All":
                    state_distinct_data = Query_Schema.state_data(db)
                    for each in state_distinct_data:
                        state_data.append(each[0])
                    data = data.filter(
                        NDTnewMortgage.mState.in_(state_data)
                    )
                else:
                    for each in request.state:
                        state_data.append(each["state"])
                    data = data.filter(
                        NDTnewMortgage.mState.in_(state_data)
                    )

            elif request.summarizeby == "County Level":
                if request.county[0]["county"] == "All" and request.county[0]["state"] != "All":
                    state_data = []
                    for each in request.county:
                        state_data.append(each["state"])
                    county_data = Query_Schema.county_data(db,county_data=state_data)
                    data = data.filter(
                        NDTnewMortgage.mState.in_(state_data),
                        NDTnewMortgage.mCounty.in_(county_data[0])
                    )
                elif request.county[0]["county"] == "All" and request.county[0]["state"] == "All":
                    state_distinct_data = Query_Schema.state_data(db)
                    state_data = []
                    for each in state_distinct_data:
                        state_data.append(each[0])
                    county_data = Query_Schema.county_data(db,county_data=state_data)
                    data = data.filter(
                        NDTnewMortgage.mState.in_(state_data),
                        NDTnewMortgage.mCounty.in_(county_data[0])
                    )
                else:
                    county_data = []
                    state_data =[]
                    for each in request.county:
                        county_data.append(each["county"])
                        state_data.append(each["state"])
                    data = data.filter(
                        NDTnewMortgage.mState.in_(state_data),
                        NDTnewMortgage.mCounty.in_(county_data)
                    )
        else:
            if state:
                data = data.filter(
                    NDTnewMortgage.mState == state
                )
            elif county:
                data = data.filter(
                    NDTnewMortgage.mState == county[1],
                    NDTnewMortgage.mCounty == county[0]
                )

        if request.isdaterange:
            if request.daterange["startdate"] and request.daterange["enddate"]:  
                start_date = request.daterange["startdate"]
                end_date = request.daterange["enddate"]
                start_date = start_date.split('-')
                start_date = (start_date[2]+"-"+start_date[0]+"-"+start_date[1])
                end_date = end_date.split('-')
                end_date = (end_date[2]+"-"+end_date[0]+"-"+end_date[1])
                data = data.filter(
                    NDTnewMortgage.mDate.between(start_date, end_date)
                )
        else:
            if year:
                data = data.filter(
                    NDTnewMortgage.mYear == year
                )
            if period:
                if period == "Annual":
                    pass
                elif period == "January":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 1
                    )
                elif period == "February":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 2
                    )
                elif period == "March":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 3
                    )
                elif period == "April":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 4
                    )
                elif period == "May":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 5
                    )
                elif period == "June":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 6
                    )
                elif period == "July":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 7
                    )
                elif period == "August":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 8
                    )
                elif period == "September":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 9
                    )
                elif period == "October":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 10
                    )
                elif period == "November":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 11
                    )
                elif period == "December":
                    data = data.filter(
                        NDTnewMortgage.mMonth == 12
                    )
                else:
                    period = period[1]
                    data = data.filter(
                        NDTnewMortgage.mQuarter == period
                    )
            
            
        if request.lenderstodisplay:
            print(f"limit: {request.lenderstodisplay}")
            data = data.limit(request.lenderstodisplay)
        # print(data.all())
  
        return data.all()


    @classmethod
    def get_all_data(cls,db):
        pmm_data = db.query(
            func.sum(NDTnewMortgage.mAmount).label("pmm_value"),
            func.count(NDTnewMortgage.mLenderName).label("pmm_count")
        ).filter(
            NDTnewMortgage.mLoanUse == "PMM"
        ).all()
        
        oth_data = db.query(
            func.sum(NDTnewMortgage.mAmount).label("oth_value"),
            func.count(NDTnewMortgage.mLenderName).label("oth_count")
        ).filter(
            NDTnewMortgage.mLoanUse == "OTH"
        ).all()
                
        return pmm_data, oth_data


class SaveQuery():

    @classmethod
    def save_query(cls,request:SaveSerializer,db):

        data =U_Queries(
            usr_id=request.usr_id,
            q_name = request.q_name,
            q_parms = str(request.model)
        )
        db.add(data)
        db.commit()

        q_id = db.query(
            U_Queries
        ).order_by(
            U_Queries.q_create_ts.desc()
        ).first()

        return q_id
    
    @classmethod
    def update_query(cls,request:UpdateSerializer,db):
        data = db.query(
            U_Queries
        ).filter(
            U_Queries.q_id == request.q_id,
            U_Queries.usr_id == request.usr_id
        )
        
        data.update({
            U_Queries.q_name : request.q_name
        })
        db.commit()
       
        return data

    # @classmethod
    # def logout_query(cls,request:LogoutSerializer,db):
        
    #     if request.q_id:
    #         to_encode = data.copy()

    #     return True   


class ListQuery():

    @classmethod
    def list_query(cls,request:LoadSerializer,db):

        data = db.query(
            U_Queries
        ).filter(
            U_Queries.usr_id==request.usr_id
        ).all()

        return data


class DeleteQuery():

    @classmethod
    def delete_query(cls,request:DeleteSerializer,db):
        data = db.query(
            U_Queries
        ).filter(
            U_Queries.q_id==request.q_id
        ).first()
        db.delete(data)
        db.commit()

        return True
