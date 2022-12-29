from sqlalchemy import or_
from src.db.database import get_db
from src.db.models import Users, NDTnewMortgage,U_Queries
from src.services.user_login1.serializer import UsersSerializer, QuerySerializer, SaveSerializer


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
    def master_query(cls,db):
        data = db.query(
            NDTnewMortgage
        )

        return data

    @classmethod
    def query(cls,
              data,
              state = None,
              county = None,
              year = None,
              lendertype = None,
              lenders = None,
              loantypessub = None
            ):


        if state:
            data = data.filter(
                NDTnewMortgage.mState.in_(state)
            )

        # final_data = final_data.first()


        if county:
            data = data.filter(or_(
                NDTnewMortgage.mCounty.in_(county),
                NDTnewMortgage.mState.in_(state)
            ))

        if year:
            data = data.filter(
                NDTnewMortgage.mYear.in_(year)
            )

        if lendertype:
            if lendertype == "Any":
                pass
            else:
                data =  data.filter(
                    NDTnewMortgage.mLenderType == lendertype
                )
        if lenders:
            data = data.filter(
                NDTnewMortgage.mLenderName.in_(lenders)
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

        return data

    @classmethod
    async def saveq(cls,request,db):
        # print("i am type",type("request"))
        saveq = U_Queries(q_parms=request)
        db.add(saveq)
        db.commit()
        db.refresh(saveq)
        return saveq
