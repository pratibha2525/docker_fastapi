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
