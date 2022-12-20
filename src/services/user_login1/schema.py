from sqlalchemy import or_
from src.db.database import get_db
from src.db.models import Users, NDTnewMortgage
from src.services.user_login1.serializer import UsersSerializer, QuerySerializer


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
            final_data = data.filter(
                NDTnewMortgage.mState.in_(state)
            )

        if county:
            final_data = data.filter(or_(
                NDTnewMortgage.mCounty.in_(county),
                NDTnewMortgage.mState.in_(state)
            ))

        if year:
            final_data = data.filter(
                NDTnewMortgage.mYear.in_(year)
            )

        if lendertype:
            if lendertype == "Any":
                pass
            else:
                final_data =  data.filter(
                    NDTnewMortgage.mLenderType == lendertype
                )

        if lenders:
            final_data = data.filter(
                NDTnewMortgage.mLenderName.in_(lenders)
            )

        if loantypessub:
            if "mARM" in loantypessub:
                final_data = data.filter(
                    NDTnewMortgage.mARM == "T"
                )

            if "mFHA" in loantypessub:
                final_data = data.filter(
                    NDTnewMortgage.mFHA == "T"
                )

            if "mHMEQ" in loantypessub:
                final_data = data.filter(
                    NDTnewMortgage.mHMEQ == "T"
                )

            if "mHELOC" in loantypessub:
                final_data = data.filter(
                    NDTnewMortgage.mHELOC == "T"
                )

            if "mReverse" in loantypessub:
                final_data = data.filter(
                    NDTnewMortgage.mReverse == "T"
                )

            if "mVHA" in loantypessub:
                final_data = data.filter(
                    NDTnewMortgage.mFHA == "T"
                )

        return final_data
