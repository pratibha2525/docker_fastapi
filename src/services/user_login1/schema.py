from sqlalchemy import or_
from src.db.database import get_db
from src.db.models import Users, NDTnewMortgage,U_Queries
from src.services.user_login1.serializer import UsersSerializer, QuerySerializer, SaveSerializer, LoadSerializer, DeleteSerializer
from sqlalchemy import func

class User_Schena():

    @classmethod
    def user_login(cls,usr_email,db):
        data = db.query(
            Users
        ).filter(
            Users.usr_email==usr_email
        ).first()

        return data

class Query_Schema():

    @classmethod
    def master_query(cls,db, request:QuerySerializer):
        pmm_data = db.query(
            NDTnewMortgage.mLenderName,
            func.sum(NDTnewMortgage.mAmount).label("pmm_value"),
            func.count(NDTnewMortgage.mLenderName).label("pmm_count")
        ).filter(
            NDTnewMortgage.mLoanUse == "PMM"
        ).group_by(NDTnewMortgage.mLenderName).subquery()
        
        oth_data = db.query(
            NDTnewMortgage.mLenderName,
            func.sum(NDTnewMortgage.mAmount).label("oth_value"),
            func.count(NDTnewMortgage.mLenderName).label("oth_count")
        ).filter(
            NDTnewMortgage.mLoanUse == "OTH"
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

        # if request.loanpurpose:
        #     data = data.filter(
                
        #     )

        
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
        
    @classmethod
    def query(cls,
              data,
              loanpurpose = None,
              usecodegroup = None,
              usecode = None,
              lendertype = None,
              loantypes = None,
              refionly = None,
              loantypessubbypass = None,
              loanmin = None,
              loanmax = None,
              allowcustomregion = None,
              t_state = None,
              t_time_period = None,
              state = None,
              county = None,
              year = None,
              lenders = None,
              loantypessub = None,
              start_date = None,
              end_date = None
            ):

        if loanpurpose:
            if loanpurpose == "Purchase":
                data = data.filter(
                    NDTnewMortgage.mLoanUse == "PMM"
                    )
            elif loanpurpose == "Non-Purchase":
                data = data.filter(
                    NDTnewMortgage.mLoanUse == "OTH"
                    )
            elif loanpurpose == "Any":
                data = data
   
        if usecodegroup:
            if usecodegroup == "ANY" and  usecode == "All":
                data = data

            elif  usecodegroup == "RES" and  usecode == "All":
                data = data.filter(
                    NDTnewMortgage.mPropType == usecodegroup
                    )
            elif  usecodegroup == "COM" and  usecode == "All":
                data = data.filter(
                    NDTnewMortgage.mPropType == usecodegroup
                    )
            else:
                usecode = usecode.upper()

                data = data.filter(
                    NDTnewMortgage.mPropType == usecodegroup,
                    NDTnewMortgage.mPropSubTP == usecode 
                    )  

        if lendertype:
            if lendertype == "Any":
                data = data
            else:
                data =  data.filter(
                    NDTnewMortgage.mLenderType == lendertype
                )
        
        if loantypes:
            if loantypes == "All":
                data = data
            elif loantypes == "Conforming":
                data =  data.filter(
                    NDTnewMortgage.mCONFORMING == "T"
                )
            elif loantypes == "Jumbo":
                data =  data.filter(
                    NDTnewMortgage.mJUMBO == "T"
                )
        
        if refionly:
            data = data.filter(
                    NDTnewMortgage.mLoanUse != "PMM"
                    )

        if loantypessub:
            if "mARM" in loantypessub:
                data = data.filter(
                    NDTnewMortgage.mARM == "T"
                )

            if "mFHA" in loantypessub:
                data = data.filter(
                    NDTnewMortgage.mFHA == "T"
                )

            if "mHMEQ" in loantypessub:
                data = data.filter(
                    NDTnewMortgage.mHMEQ == "T"
                )

            if "mHELOC" in loantypessub:
                data = data.filter(
                    NDTnewMortgage.mHELOC == "T"
                )

            if "mReverse" in loantypessub:
                data = data.filter(
                    NDTnewMortgage.mReverse == "T"
                )

            if "mVHA" in loantypessub:
                data = data.filter(
                    NDTnewMortgage.mFHA == "T"
                )
                
        if loantypessubbypass:
            data = data.filter(
                    NDTnewMortgage.mHELOC == "T",
                    NDTnewMortgage.mHMEQ == "T",
                    NDTnewMortgage.mLoanUse != "PMM"
                    )

        if loanmin or loanmax:
            if loanmin != "" and loanmax == "":
                data = data.filter(
                    NDTnewMortgage.mAmount >= int(loanmin),
                    )
            elif loanmax != "" and loanmin == "":
                data = data.filter(
                    NDTnewMortgage.mAmount <= int(loanmax),
                    )
            elif loanmin != "" and loanmax != "":
                data = data.filter(
                    NDTnewMortgage.mAmount.between(int(loanmin),int(loanmax)),
                    )
        
        
        if allowcustomregion:

            if t_state and t_time_period:
                data = data.filter(
                        NDTnewMortgage.mState.in_(t_state)
                        )
                # print(t_state)
                # all_data = []
                # for period in t_time_period:
                #     if period == "Q1":
                #         row_period = int(period[1].split("Q")[1])
                #     elif period == "Q2":
                #         row_period = int(period[1].split("Q")[1])
                #     elif period == "Q3":
                #         row_period = int(period[1].split("Q")[1])
                #     elif period == "Q4":
                #         row_period = int(period[1].split("Q")[1])

                #         all_data.append(data)
            # return all_data

        if state:
            data = data.filter(
                NDTnewMortgage.mState.in_(state)
            )

        if county:
            data = data.filter(or_(
                NDTnewMortgage.mCounty.in_(county),
                NDTnewMortgage.mState.in_(state)
            ))

        if year:
            data = data.filter(
                NDTnewMortgage.mYear.in_(year)
            )

        if start_date and end_date:
            data = data.filter(
                NDTnewMortgage.mDate.between(start_date,end_date)
            )

        if lenders:
            data = data.filter(
                NDTnewMortgage.mLenderName.in_(lenders)
            )



        return data

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
