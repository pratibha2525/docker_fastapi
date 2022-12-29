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


    
    
# 2nd database

class Users(Base):
    __tablename__ = "users"
    usr_id = db.Column(db.Integer,primary_key=True,index=True)
    usr_username = db.Column(db.String,nullable=False)
    usr_password = db.Column(db.String,nullable=False)
    usr_email = db.Column(db.String,nullable=True)
    usr_status= db.Column(db.String,nullable=False,default ='a')
    usr_admin= db.Column(db.String ,nullable=False,default ='n')
    usr_valid_until = db.Column(db.DateTime,nullable=True)
    usr_fname =db.Column(db.String ,nullable=True)
    usr_lname=db.Column(db.String ,nullable=True)
    usr_addr1=db.Column(db.String ,nullable=True)
    usr_addr2 =db.Column(db.String ,nullable=True)
    usr_city =db.Column(db.String ,nullable=True)
    usr_state =db.Column(db.String ,nullable=True)
    usr_zip = db.Column(db.String ,nullable=True)
    usr_company =db.Column(db.String ,nullable=True)
    usr_logo =db.Column(db.String ,nullable=True)
    usr_create_ts = db.Column(db.DateTime,default=datetime.now)
    usr_parms=db.Column(db.Text,nullable=True)




# /// Query_Save_Store


class U_Queries(Base):
    __tablename__ = "u_queries"
    q_id= db.Column(db.Integer,primary_key=True,index=True)
    usr_id = db.Column(db.Integer,nullable=False)
    q_name =db.Column(db.String,nullable=True) 
    q_create_ts =db.Column(db.DateTime,default=datetime.now)
    q_lastmod = db.Column(db.DateTime,default=datetime.now)
    q_parms = db.Column(db.Text,nullable=True)


class Track_Usage_Msm(Base):
    __tablename__ = "track_usage_msm"
    msm_u_id =db.Column(db.Integer,primary_key=True,index=True)
    usr_id = db.Column(db.Integer,nullable=False)
    create_ts = db.Column(db.DateTime, default=datetime.now)
    parms =db.Column(db.Text,nullable=True)


class BK_New_Mortgage(Base):
    __tablename__ = "BK.new_mortgage"
    id = db.Column(db.Integer,primary_key=True,index=True)
    mState =db.Column(db.String ,nullable=True)
    mCounty =db.Column(db.String ,nullable=True)
    mCity =db.Column(db.String,nullable=True)
    mZipcode =db.Column(db.String ,nullable=True)
    mCensusTrac =db.Column(db.String ,nullable=True)
    mPropType =db.Column(db.String ,nullable=True)
    mDate=  db.Column(db.DateTime,nullable=True)
    mYear = db.Column(db.Integer,nullable=True) 
    mMonth= db.Column(db.Integer,nullable=True)
    mQuarter =db.Column(db.Integer,nullable=True)
    mLenderName = db.Column(db.String ,nullable=True)
    mAmount =db.Column(db.Integer,nullable=True)
    mVHA = db.Column(db.String ,nullable=True)
    mFHA= db.Column(db.String ,nullable=True)
    mReverse = db.Column(db.String ,nullable=True)
    mARM = db.Column(db.String ,nullable=True)
    mHMEQ = db.Column(db.String ,nullable=True)
    mHELOC = db.Column(db.String ,nullable=True)
    mCONFORMING = db.Column(db.String ,nullable=True)
    mJUMBO= db.Column(db.String ,nullable=True)
    mLoanUse = db.Column(db.String ,nullable=True)
    mLenderType = db.Column(db.String,nullable=True)
    mPropSubTP = db.Column(db.String ,nullable=True)
    mTRANID = db.Column(db.String ,nullable=True)
    mOrigID= db.Column(db.String ,nullable=True)
    mOrigName = db.Column(db.String ,nullable=True)
    mLDRPhone= db.Column(db.String ,nullable=True)
    mDocNum = db.Column(db.String,nullable=True)
    mBook = db.Column(db.String,nullable=True)
    mPage = db.Column(db.String,nullable=True)
    mMultiAPN = db.Column(db.String,nullable=True)
    mRecordType = db.Column(db.String,nullable=True)
    mLUDate = db.Column(db.DateTime,default=datetime.now)





class LONameTbl(Base):
    __tablename__ = "LONameTbl"
    h_id= db.Column(db.Integer,primary_key=True,index=True)
    mOrigID = db.Column(db.String ,nullable=True)
    mOrigName = db.Column(db.String ,nullable=True)
    Num = db.Column(db.Integer,nullable=True)
    dts=db.Column(db.DateTime,default=datetime.now)





class NMLSContact(Base):
    __tablename__ = "NMLSContact"
    t_id=db.Column(db.Integer,primary_key=True,index=True)
    LID =db.Column(db.Integer,nullable=False)
    cFL_LO = db.Column(db.String,nullable=False)
    cFL_CompanyID=db.Column(db.String,nullable=False)
    cFL_LOName = db.Column(db.String,nullable=True)
    cFL_CompanyName = db.Column(db.String,nullable=True)
    cFL_Address=db.Column(db.String,nullable=True)
    cFL_CompanyWebsite =db.Column(db.String,nullable=True)
    cFL_WorkEmail=db.Column(db.String,nullable=True)
    cFL_PersonalEmail=db.Column(db.String ,nullable=True)
    cFL_LO_Status=db.Column(db.String,nullable=True)
    cFL_LOID_CID =db.Column(db.String ,nullable=True)
    LOOrgID = db.Column(db.BigInteger,index=True,nullable=True)
    LOOrgName =db.Column(db.String,nullable=True)
    Collected_EmployerCOMPANY =db.Column(db.String ,nullable=True)
    Collected_EmployerCOMPANYID=db.Column(db.BigInteger,index=True)
    Collected_Employer_Type =db.Column(db.String,nullable=True)
    Collected_EmployerAddress =db.Column(db.String,nullable=True)
    Collected_EmployerCity =db.Column(db.String,nullable=True)
    Collected_EmployerState =db.Column(db.String,nullable=True)
    Collected_EmployerZip =db.Column(db.String,nullable=True)
    AddressType =db.Column(db.String,nullable=True)
    Collected_OfficePhone =db.Column(db.String,nullable=True)
    Collected_OfficePhoneExt =db.Column(db.String ,nullable=True)
    Collected_CellPhone =db.Column(db.String,nullable=True)
    Collected_WorkEmail =db.Column(db.String,nullable=True)
    Collected_PersonalEmail = db.Column(db.String,nullable=True)
    Collected_EmployerWebsite =db.Column(db.String,nullable=True)
    Collected_LOWebSite=db.Column(db.String ,nullable=True)
    Collected_Linkedin=db.Column(db.String ,nullable=True)
    Collected_Twitter=db.Column(db.String ,nullable=True)
    Collected_Facebook=db.Column(db.String ,nullable=True)
    Collected_Other=db.Column(db.String ,nullable=True)



# 4th databse

class NDTnewMortgage(Base):
    __tablename__ = "NDT.new_mortgage"
    id = db.Column(db.Integer,primary_key=True,index=True)
    mState = db.Column(db.String ,nullable=True)
    mCounty = db.Column(db.String ,nullable=True)
    mCity = db.Column(db.String ,nullable=True)
    mZipcode = db.Column(db.String,nullable=True)
    mCensusTrac = db.Column(db.String,nullable=True)
    mPropType = db.Column(db.String ,nullable=True)
    mDate = db.Column(db.DateTime,nullable=True)
    mYear =db.Column(db.Integer,nullable=True)
    mMonth =db.Column(db.Integer,nullable=True)
    mQuarter=db.Column(db.Integer,nullable=True)
    mLenderName =db.Column(db.String ,nullable=True)
    mAmount=db.Column(db.Integer,nullable=True)
    mVHA =db.Column(db.String ,nullable=True)
    mFHA =db.Column(db.String ,nullable=True)
    mReverse =db.Column(db.String ,nullable=True)
    mARM =db.Column(db.String ,nullable=True)
    mHMEQ =db.Column(db.String ,nullable=True)
    mHELOC =db.Column(db.String ,nullable=True)
    mCONFORMING =db.Column(db.String ,nullable=True)
    mJUMBO =db.Column(db.String ,nullable=True)
    mLoanUse =db.Column(db.String ,nullable=True)
    mLenderType =db.Column(db.String ,nullable=True)
    mPropSubTP =db.Column(db.String ,nullable=True)
    mTRANID=db.Column(db.Integer,nullable=True)
    mOrigID =db.Column(db.String ,nullable=True)
    mOrigName =db.Column(db.String ,nullable=True)
    mLDRPhone =db.Column(db.String ,nullable=True)
    mBrokerID =db.Column(db.String ,nullable=True)
    mBrokerName =db.Column(db.String ,nullable=True)
    mLOOrgName =db.Column(db.String ,nullable=True)
    mLOOrgID =db.Column(db.String ,nullable=True)
  
class County(Base):
    __tablename__ = "county"
    countyid = db.Column(db.Integer,primary_key=True)
    state = db.Column(db.String)
    County = db.Column(db.String)
 
class City(Base):
    __tablename__ = "city"
    cityid = db.Column(db.Integer,primary_key=True)
    state = db.Column(db.String)
    County = db.Column(db.String)
    city = db.Column(db.String)
 
class Lenders(Base):
    __tablename__ = "lenders"
    lenderid = db.Column(db.Integer,primary_key=True)
    lenderType = db.Column(db.String)
    lenderName = db.Column(db.String)

class LenderNameSubTblv1(Base):
    __tablename__ = "LenderNameSubTblv1"
    
    UID = db.Column(db.Integer,primary_key=True)
    OrgLender = db.Column(db.String)
    StdLender = db.Column(db.String)
    TWGLTCode = db.Column(db.Integer,primary_key=True)

class LenderTypeSubTblv1(Base):
    __tablename__ = "LenderTypeSubTblv1"
    
    TWGLTCode = db.Column(db.Integer,primary_key=True)
    TWGLenderType = db.Column(db.String)
