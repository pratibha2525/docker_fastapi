from sqlalchemy import or_
from src.db.database import get_db
from src.db.models import Lo_Users, U_Loqueries
from src.services.loan_module.serializer import Lo_UsersSerializer, SaveSerializer,UpdateSerializer,DeleteSerializer,LoadSerializer


class User_Schema():

    @classmethod
    def user_login(cls,usr_email,db):
        data = db.query(
            Lo_Users
        ).filter(
            Lo_Users.usr_email==usr_email
        ).first()

        return data

# class Query_Schema():

#     @classmethod
#     def master_query(cls,db):
#         data = db.query(
#             NDTnewMortgage
#         )

#         return data

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
