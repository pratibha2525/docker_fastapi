from sqlalchemy import or_
from src.db.database import get_db
from src.db.models import Lo_Users, U_Loqueries, BK_New_Mortgage
from src.services.loan_module.serializer import Lo_UsersSerializer,QuerySerializer, SaveSerializer,UpdateSerializer,DeleteSerializer,LoadSerializer
from sqlalchemy import func
import sqlalchemy

class User_Schema():

    @classmethod
    def user_login(cls,usr_email,db):
        data = db.query(
            Lo_Users
        ).filter(
            Lo_Users.usr_email==usr_email
        ).first()

        return data

class Query_Schema():
    
    @classmethod
    def state_data(cls,db):
        data = db.query(
            BK_New_Mortgage.mState
        ).distinct().all()
        
        return data

    @classmethod
    def county_data(cls,db,county_data):
        data = db.query(
            BK_New_Mortgage.mCounty,
            BK_New_Mortgage.mState
        ).filter(
            BK_New_Mortgage.mState.in_(county_data)
        ).distinct().all()
        
        return data
    
    @classmethod
    def get_all_data(cls,db):
        pmm_data = db.query(
            func.count(BK_New_Mortgage.mLenderName).label("num_loans"),
            func.sum(BK_New_Mortgage.mAmount).label("total_amount")
        ).filter(
            BK_New_Mortgage.mLoanUse == "PMM",
            BK_New_Mortgage.mOrigName != None,
            BK_New_Mortgage.mOrigID is not None,
            BK_New_Mortgage.mLenderName.not_ilike('Misc%')
        ).all()
        
        oth_data = db.query(
            func.count(BK_New_Mortgage.mLenderName).label("x_num"),
            func.sum(BK_New_Mortgage.mAmount).label("x_amt")
        ).filter(
            BK_New_Mortgage.mLoanUse == "OTH",
            BK_New_Mortgage.mOrigName != None,
            BK_New_Mortgage.mOrigID is not None,
            BK_New_Mortgage.mLenderName.not_ilike('Misc%')
        ).all()
                
        return pmm_data, oth_data
    
    @classmethod
    def master_query(cls, db, request:QuerySerializer, year = None, period = None, state = None, county = None):

        pmm_data = db.query(
            BK_New_Mortgage.mOrigID,
            func.count(BK_New_Mortgage.mLenderName).label("num_loans"),
            func.sum(BK_New_Mortgage.mAmount).label("total_amount")
        ).filter(
            # BK_New_Mortgage.mLoanUse == "PMM",
            BK_New_Mortgage.mOrigName.is_not(None),
            BK_New_Mortgage.mOrigID.is_not(None),
            BK_New_Mortgage.mLenderName.not_ilike('Misc%')
        ).group_by(
            BK_New_Mortgage.mLenderName,
            BK_New_Mortgage.mOrigID
        ).subquery()

        oth_data = db.query(
            BK_New_Mortgage.mOrigID,
            func.count(BK_New_Mortgage.mLenderName).label("x_num"),
            func.sum(BK_New_Mortgage.mAmount).label("x_amt"),
        ).filter(
            BK_New_Mortgage.mLoanUse == "OTH",
            BK_New_Mortgage.mOrigName.is_not(None),
            BK_New_Mortgage.mOrigID.is_not(None),
            BK_New_Mortgage.mLenderName.not_ilike('Misc%')
        ).group_by(
            BK_New_Mortgage.mLenderName,
            BK_New_Mortgage.mOrigID
        ).subquery()

        data = db.query(
            BK_New_Mortgage.mOrigName,
            BK_New_Mortgage.mOrigID,
            BK_New_Mortgage.mLenderName,
            pmm_data,
            oth_data
        ).outerjoin(
            pmm_data,
            pmm_data.c.mOrigID == BK_New_Mortgage.mOrigID
        ).outerjoin(
            oth_data,
            oth_data.c.mOrigID == BK_New_Mortgage.mOrigID
        ).group_by(BK_New_Mortgage.mOrigName,
            BK_New_Mortgage.mOrigID,
            BK_New_Mortgage.mLenderName,pmm_data,oth_data)
        
        print("i am row data :- ,",data)

        # if request.reportrank == "# Loans":
        #     print(f"Report Rank: Loans")
        #     data = data.order_by(func.count(BK_New_Mortgage.mLenderName).desc())
        # elif request.reportrank == "$ Volume":
        #     print(f"Report Rank: Volumes")
        #     data = data.order_by(func.sum(BK_New_Mortgage.mAmount).desc())

        # print(f"Loan Purpose : {request.loanpurpose}")
        # if request.loanpurpose == "Purchase":
        #     data = data.filter(
        #         BK_New_Mortgage.mLoanUse == "PMM"
        #     ).order_by(func.sum(BK_New_Mortgage.mAmount).desc())
        # elif request.loanpurpose == "Non-Purchase":
        #     data = data.filter(
        #         BK_New_Mortgage.mLoanUse == "OTH"
        #     ).order_by(func.sum(BK_New_Mortgage.mAmount).desc())

        # if request.usecode:
        #     print(f"Usecode {request.usecode}")
        #     if  request.usecode["usecodegroup"] == "RES" and  request.usecode["usecode"] == "All":
        #         data = data.filter(
        #             BK_New_Mortgage.mPropType == request.usecode["usecodegroup"]
        #         )
        #     elif  request.usecode["usecodegroup"] == "COM" and  request.usecode["usecode"] == "All":
        #         data = data.filter(
        #             BK_New_Mortgage.mPropType == request.usecode["usecodegroup"]
        #             )
        #     elif request.usecode["usecodegroup"] == "ANY" and  request.usecode["usecode"] == "All":
        #         data = data
        #     else:
        #         usecode = request.usecode["usecode"].upper()
        #         data = data.filter(
        #             BK_New_Mortgage.mPropType == request.usecode["usecodegroup"],
        #             BK_New_Mortgage.mPropSubTP == usecode 
        #         )
                
        # if request.lendertype:
        #     if request.lendertype == "Any":
        #         data = data
        #     else:
        #         data =  data.filter(
        #             BK_New_Mortgage.mLenderType == request.lendertype
        #         )
                
        # if request.lenders:
        #     data = data.filter(
        #         BK_New_Mortgage.mLenderName.in_(request.lenders)
        #     )
        
        # if request.loantypes:
        #     if request.loantypes == "All":
        #         data = data
        #     elif request.loantypes == "Conforming":
        #         data =  data.filter(
        #             BK_New_Mortgage.mCONFORMING == "T"
        #         )
        #     elif request.loantypes == "Jumbo":
        #         data =  data.filter(
        #             BK_New_Mortgage.mJUMBO == "T"
        #         )

        # if request.loantypessub:
        #     if "ARM" in request.loantypessub:
        #         data = data.filter(
        #             BK_New_Mortgage.mARM == "T"
        #         )

        #     if "FHA" in request.loantypessub:
        #         data = data.filter(
        #             BK_New_Mortgage.mFHA == "T"
        #         )

        #     if "Home Equity Loan" in request.loantypessub:
        #         data = data.filter(
        #             BK_New_Mortgage.mHMEQ == "T"
        #         )

        #     if "HELOC" in request.loantypessub:
        #         data = data.filter(
        #             BK_New_Mortgage.mHELOC == "T"
        #         )

        #     if "Reverse" in request.loantypessub:
        #         data = data.filter(
        #             BK_New_Mortgage.mReverse == "T"
        #         )

        #     if "VHA" in request.loantypessub:
        #         data = data.filter(
        #             BK_New_Mortgage.mFHA == "T"
        #         )
        
        # if request.refionly:
        #     if request.refionly == True:
        #         data = data.filter(
        #             BK_New_Mortgage.mHMEQ == "F",
        #             BK_New_Mortgage.mHELOC == "F"
        #         )
        
        # if request.excl_usahud:
        #     if request.excl_usahud == True:
        #         data = data.filter(
        #             BK_New_Mortgage.mLenderName != "USA Housing and Urban Development",
        #             BK_New_Mortgage.mLenderName != "DEPARTMENT OF HOUSING & URBAN DEV"
        #         )

        # if request.loantypessubbypass:
        #     if request.loantypessubbypass == True:
        #         data = data.filter(
        #                 BK_New_Mortgage.mHELOC == "T",
        #                 BK_New_Mortgage.mHMEQ == "T",
        #                 )
        
        # if request.customregion:
        #     if request.summarizeby == "State Level":
        #         state_data = []
        #         if request.state[0]["state"] == "All":
        #             state_distinct_data = Query_Schema.state_data(db)
        #             for each in state_distinct_data:
        #                 state_data.append(each[0])
        #             data = data.filter(
        #                 BK_New_Mortgage.mState.in_(state_data)
        #             )
        #         else:
        #             for each in request.state:
        #                 state_data.append(each["state"])
        #             data = data.filter(
        #                 BK_New_Mortgage.mState.in_(state_data)
        #             )

        #     elif request.summarizeby == "County Level":
        #         if request.county[0]["county"] == "All" and request.county[0]["state"] != "All":
        #             state_data = []
        #             for each in request.county:
        #                 state_data.append(each["state"])
        #             county_data = Query_Schema.county_data(db,county_data=state_data)
        #             data = data.filter(
        #                 BK_New_Mortgage.mState.in_(state_data),
        #                 BK_New_Mortgage.mCounty.in_(county_data[0])
        #             )
        #         elif request.county[0]["county"] == "All" and request.county[0]["state"] == "All":
        #             state_distinct_data = Query_Schema.state_data(db)
        #             state_data = []
        #             for each in state_distinct_data:
        #                 state_data.append(each[0])
        #             county_data = Query_Schema.county_data(db,county_data=state_data)
        #             data = data.filter(
        #                 BK_New_Mortgage.mState.in_(state_data),
        #                 BK_New_Mortgage.mCounty.in_(county_data[0])
        #             )
        #         else:
        #             county_data = []
        #             state_data =[]
        #             for each in request.county:
        #                 county_data.append(each["county"])
        #                 state_data.append(each["state"])
        #             data = data.filter(
        #                 BK_New_Mortgage.mState.in_(state_data),
        #                 BK_New_Mortgage.mCounty.in_(county_data)
        #             )
        # else:
        #     if state:
        #         data = data.filter(
        #             BK_New_Mortgage.mState == state
        #         )
        #     elif county:
        #         data = data.filter(
        #             BK_New_Mortgage.mState == county[1],
        #             BK_New_Mortgage.mCounty == county[0]
        #         )

        # if request.isdaterange:
        #     if request.daterange["startdate"] and request.daterange["enddate"]:  
        #         start_date = request.daterange["startdate"]
        #         end_date = request.daterange["enddate"]
        #         start_date = start_date.split('-')
        #         start_date = (start_date[2]+"-"+start_date[0]+"-"+start_date[1])
        #         end_date = end_date.split('-')
        #         end_date = (end_date[2]+"-"+end_date[0]+"-"+end_date[1])
        #         data = data.filter(
        #             BK_New_Mortgage.mDate.between(start_date, end_date)
        #         )
        # else:
        #     if year:
        #         data = data.filter(
        #             BK_New_Mortgage.mYear == year
        #         )
        #     if period:
        #         if period == "Annual":
        #             pass
        #         elif period == "January":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 1
        #             )
        #         elif period == "February":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 2
        #             )
        #         elif period == "March":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 3
        #             )
        #         elif period == "April":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 4
        #             )
        #         elif period == "May":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 5
        #             )
        #         elif period == "June":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 6
        #             )
        #         elif period == "July":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 7
        #             )
        #         elif period == "August":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 8
        #             )
        #         elif period == "September":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 9
        #             )
        #         elif period == "October":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 10
        #             )
        #         elif period == "November":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 11
        #             )
        #         elif period == "December":
        #             data = data.filter(
        #                 BK_New_Mortgage.mMonth == 12
        #             )
        #         else:
        #             period = period[1]
        #             data = data.filter(
        #                 BK_New_Mortgage.mQuarter == period
        #             )
            
            
        if request.lenderstodisplay:
            print(f"limit: {request.lenderstodisplay}")
            data = data.limit(request.lenderstodisplay)
        
        print(data.all())
  
        return data.all()


class SaveQuery():

    @classmethod
    def save_query(cls,request:SaveSerializer,db):

        data =U_Loqueries(
            usr_id=request.usr_id,
            q_name = request.q_name,
            q_parms = str(request.model)
        )
        db.add(data)
        db.commit()

        q_id = db.query(
            U_Loqueries
        ).order_by(
            U_Loqueries.q_create_ts.desc()
        ).first()

        return q_id

    @classmethod
    def update_query(cls,request:UpdateSerializer,db):
        data = db.query(
            U_Loqueries
        ).filter(
            U_Loqueries.q_id == request.q_id,
            U_Loqueries.usr_id == request.usr_id
        )
        
        data.update({
            U_Loqueries.q_name : request.q_name
        })
        db.commit()
       
        return data

class DeleteQuery():

    @classmethod
    def delete_query(cls,request:DeleteSerializer,db):
        data = db.query(
            U_Loqueries
        ).filter(
            U_Loqueries.q_id==request.q_id
        ).first()
        db.delete(data)
        db.commit()

        return True

class ListQuery():

    @classmethod
    def list_query(cls,request:LoadSerializer,db):

        data = db.query(
            U_Loqueries
        ).filter(
            U_Loqueries.usr_id==request.usr_id
        ).all()

        return data
