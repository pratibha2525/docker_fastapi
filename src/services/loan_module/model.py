import sqlalchemy as db
from datetime import datetime

from src.db.database import Base

class Lo_Users(Base):
    __tablename__ = "lo_users"
    usr_id = db.Column(db.Integer,primary_key=True,index=True)
    usr_username = db.Column(db.String,nullable=False)
    usr_password = db.Column(db.String,nullable=False)
    usr_email= db.Column(db.String,nullable=True)
    usr_status= db.Column(db.String,nullable=False,default ='a')
    usr_admin= db.Column(db.String,nullable=False,default='n')
    usr_valid_until = db.Column(db.DateTime,nullable=True)
    usr_fname = db.Column(db.String,nullable=True)
    usr_lname =db.Column(db.String,nullable=True)
    usr_addr1 = db.Column(db.String,nullable=True)
    usr_addr2 = db.Column(db.String,nullable=True)
    usr_city = db.Column(db.String,nullable=True)
    usr_state =db.Column(db.String,nullable=True)
    usr_zip= db.Column(db.String,nullable=True)
    usr_company =db.Column(db.String,nullable=True)
    usr_logo = db.Column(db.String,nullable=True)
    usr_create_ts = db.Column(db.DateTime,default=datetime.now)
    usr_parms= db.Column(db.Text,nullable=True)
    usr_sso = db.Column(db.Text,nullable=True)


class U_Loqueries(Base):
    __tablename__ = "u_lo_queries"
    q_id = db.Column(db.Integer,primary_key=True,index=True)
    usr_id = db.Column(db.Integer,nullable=False)
    q_name = db.Column(db.String,nullable=True)
    q_create_ts = db.Column(db.DateTime,default=datetime.now)
    q_lastmod = db.Column(db.DateTime ,default=datetime.now)
    q_parms = db.Column(db.Text,nullable=True)

# /// Query_Log

class Track_Usage_Lo(Base):
    __tablename__ = "track_usage_lo"
    msm_u_id = db.Column(db.Integer,primary_key=True,index=True)
    usr_id =db.Column(db.Integer,nullable=False)
    create_ts= db.Column(db.DateTime,default=datetime.now)
    parms = db.Column(db.Text,nullable=True)
