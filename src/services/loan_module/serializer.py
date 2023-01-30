from pydantic import BaseModel, constr
from pydantic.types import constr, conint
from typing import Optional, List

##### LOAN ORIGINATOR MODULE (login, run_query, save_query, load_query) #####

class Lo_UsersSerializer(BaseModel):
    usr_username: constr(min_length=1)
    usr_email: str
    usr_password: str

class QuerySerializer(BaseModel):
        allowcustomregion: Optional[bool] = True # I am not sure about this
        reportformat: Optional[constr(min_length=1)] = "HTML"
        reporttype: Optional[constr(min_length=1)] = "Ranking Report"
        lt = {
                "lendertype": Optional[constr(min_length=1)],
                "lendertypesetup": Optional[bool]
        }
        reporting: Optional[dict] = {}
        censustract: Optional[list] # Not mapped in web 
        
        reportrank: constr(min_length=1) = "$ Volume"
        pmmnonpmm: Optional[constr(min_length=1)] = "Any"
        usecode = {
            "id": int,
            "usecode": str,
            "usecodegroup": str
        }
        addgroup: Optional[constr(min_length=1)] = "Any" # Government, Conventional / 
        
        lendertype: Optional[constr(min_length=1)] = "Any"
        lenderstodisplay: Optional[constr(min_length=1)] = "5"
        nmlsid: Optional[constr(min_length=0)] = ""
        
        loanmax: Optional[constr(min_length=0)]
        loanmin: Optional[constr(min_length=0)]
        refionly: Optional[bool] = True
        loantypessubbypass: Optional[bool] = False
        
        summarizeby: Optional[constr(min_length=1)] = "Nationwide" # State Level , County Level
        customregion: Optional[bool] = False
        state: Optional[list] = []
        county: Optional[list] = []
        isdaterange : Optional[bool] = False
        daterange = {
            "startdate": Optional[constr(min_length=0)],
            "enddate": Optional[constr(min_length=0)]
        }

        year: Optional[List] = []
        period: Optional[List] = []
        
        citytown: Optional[list]    # Not mapped in web
        zipcode: Optional[list]     # Not mapped in web

class SaveSerializer(BaseModel):
    q_name: str
    usr_id: int
    model = {
        "addgroup": constr(min_length=1),
        "allowcustomregion": bool,
        "censustract": list,
        "citytown": list,
        "couty": list,
        "customregion": bool,
        "lenderstodisplay": constr(min_length=1),
        "lendertype": constr(min_length=1),
        "loanmax": constr(min_length=0),
        "loanmin": constr(min_length=0),
        "loantypessubbypass": bool,
        "lt": {
            "lendertype": str,
            "lendertypesetup": bool
        },
        "nmlsid": constr(min_length=0),
        "period": list,
        "pmmnonpmm": constr(min_length=1),
        "refionly": bool,
        "reportformat": constr(min_length=1),
        "reporting": dict,
        "reportrank": constr(min_length=1),
        "reporttype": constr(min_length=1),
        "state": list,
        "summarizeby": constr(min_length=1),
        "usecode": {
                "_uiSelectChoiceDisabled": bool,
                "id": int,
                "usecode": str,
                "usecodegroup": str
        },
        "year": list,
        "zipcode": list
    }

class UpdateSerializer(BaseModel):
    q_id: Optional[conint()]
    usr_id: Optional[conint()]
    q_name : Optional[constr(min_length=1)]

class DeleteSerializer(BaseModel):
    q_id: int
    usr_id: int

class LoadSerializer(BaseModel):
    usr_id: int
    
class CsvSerializer(BaseModel):
    # cur_report_ary: list
    # cur_report_header_ary: list
    exporttype: str
    # brokerflag: bool
