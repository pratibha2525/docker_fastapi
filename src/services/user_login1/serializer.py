from pydantic import BaseModel, constr
from pydantic.types import constr, conint
from typing import Optional, List

##### MSM MARKET SHARE MODULE (login, run_query, save_query, load_query) #####

class UsersSerializer(BaseModel):
    usr_username: constr(min_length=1)
    usr_email: str
    usr_password: str


# {
#   "reporttype": "Ranking Report",
#   "reportrank": "# Loans",
#   "reportformat": "HTML",
#   "brokerlenderbypass": false,
#    "customregion": false,
#    "excl_usahud": false,
#    "loantypessubbypass": true,
#    "refionly": true,
#    "isdaterange":false,
#    "daterange":{
#    },
#   "usecode": {
#     "id": 2,
#     "usecodegroup": "RES",
#     "usecode": "1-Family",
#     "_uiSelectChoiceDisabled": false
#   },
#   "loanpurpose": "Any",
#   "lendertype": "Banks",
#   "lenderstodisplay": "5",
#   "lenders": [],
#   "ltext": "",
#   "loantypes": "Conforming",
#   "loantypessub": [
#     "Home Equity Loan"
#   ],
#   "loanmin": "111",
#   "loanmax": "",
#   "summarizeby": "State Level",
#   "allowcustomregion": true,
#   "state": [
#     {
#       "state": "AK",
#       "_uiSelectChoiceDisabled": false
#     },
#     {
#       "state": "AZ",
#       "_uiSelectChoiceDisabled": false
#     }
#   ],
#   "county": [],
#   "citytown": [],
#   "zipcode": [],
#   "censustract": [],
#   "year": [
#     "2021",
#     "2022"
#   ],
#   "period": [
#     "Q1",
#     "Q3"
#   ],
#   "reporting": {},
#   "lt": {
#     "lendertypesetup": true
#   }
# }




class QuerySerializer(BaseModel):
    allowcustomregion: Optional[bool] = True # I am not sure about this
    reporttype: Optional[constr(min_length=1)] = "Ranking Report"
    reportrank: constr(min_length=1) = "$ Volume"
    reportformat: Optional[constr(min_length=1)] = "HTML"
    reporting: Optional[dict] = {}
    ltext: Optional[constr(min_length=0)] = ""

    loanpurpose: Optional[constr(min_length=1)] = "Any"
    usecode = {
        "_uiSelectChoiceDisabled": Optional[bool],
        "id": Optional[int],
        "usecode": Optional[str],
        "usecodegroup": Optional[str]
    }
    lendertype: Optional[constr(min_length=1)] = "Any"
    lenderstodisplay: Optional[constr(min_length=1)] = "5"
    lenders: Optional[list] = []
    
    loantypes: Optional[constr(min_length=1)] = "All"
    loantypessub: Optional[list] = []                              
    refionly: Optional[bool] = True
    excl_usahud: Optional[bool] = True
    loantypessubbypass: Optional[bool] = False
    loanmax: Optional[constr(min_length=0)]
    loanmin: Optional[constr(min_length=0)]
    
    
    customregion: Optional[bool] = False
    state: Optional[list] = []
    summarizeby: Optional[constr(min_length=1)] = "State Level" # County Level
    county: Optional[list] = []
    year: Optional[List] = []
    period: Optional[List] = []
    isdaterange : Optional[bool] = False
    daterange = {
        "startdate": Optional[constr(min_length=0)],
        "enddate": Optional[constr(min_length=0)]
    }
    
    brokerlenderbypass: Optional[bool] = False # Remaining

    censustract: Optional[list] # Not mapped in web
    citytown: Optional[list]    # Not mapped in web
    zipcode: Optional[list]     # Not mapped in web
    lt = {
        "lendertypesetup": Optional[bool]
    }


class SaveSerializer(BaseModel):
    q_name: str
    usr_id: int
    model = {
        "allowcustomregion": bool,
        "brokerlenderbypass": bool,
        "censustract": list,
        "citytown": list,
        "county": list,
        "customregion": bool,
        "excl_usahud": bool,
        "isdaterange" : bool,
        "lenders": list,
        "lenderstodisplay": constr(min_length=1),
        "lendertype": constr(min_length=1),
        "loanmax": constr(min_length=0),
        "loanmin": constr(min_length=0),
        "loanpurpose": constr(min_length=1),
        "loantypes": constr(min_length=1),
        "loantypessub": list,
        "loantypessubbypass": bool,
        "lt" : {
            "lendertypesetup": bool
        },
        "ltext": constr(min_length=0),
        "period": list,
        "refionly": bool,
        "reportformat": constr(min_length=1),
        "reporting": dict,
        "reportrank": constr(min_length=1),
        "reporttype": constr(min_length=1),
        "state": list,
        "summarizeby": constr(min_length=1),
        "usecode" : {
            "_uiSelectChoiceDisabled": bool,
            "id": int,
            "usecode": str,
            "usecodegroup": str
        },
        "daterange" : {
                "startdate": constr(min_length=0),
                "enddate": constr(min_length=0)
            },
        "year": list,
        "zipcode": list
    }

class UpdateSerializer(BaseModel):
    q_id: Optional[conint()]
    usr_id: Optional[conint()]
    q_name : Optional[constr(min_length=1)]

class LogoutSerializer(BaseModel):
    q_id: conint()
    # acces_token: constr(min_length=1)

class LoadSerializer(BaseModel):
    usr_id: int
    
class DeleteSerializer(BaseModel):
    q_id: int
    usr_id: int

class CsvSerializer(BaseModel):
    cur_report_ary: list
    cur_report_header_ary: list
    exporttype: str
    brokerflag: bool
