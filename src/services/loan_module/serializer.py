from pydantic import BaseModel, constr
from pydantic.types import constr, conint
from typing import Optional, List

##### LOAN ORIGINATOR MODULE (login, run_query, save_query, load_query) #####

class Lo_UsersSerializer(BaseModel):
    usr_username: constr(min_length=1)
    usr_email: str
    usr_password: str

# class QuerySerializer(BaseModel):
#     addgroup : str
#     allowcustomregion : bool
#     censustract : list
#     citytown : list
#     county : list
#     customregion : bool
#     lenderstodisplay : constr(min_length=1)
#     lendertype : constr(min_length=1)
#     loanmax : constr(min_length=1)
#     loanmin : constr(min_length=1)
#     loantypessubbypass : bool
#     lt = {
#              "lendertype": str ,
#             "lendertypesetup": bool
#         }
#     nmlsid : constr(min_length=1)
#     period : list
#     pmmnonpmm : str
#     refionly : bool
#     reportformat : constr(min_length=1)
#     reporting : dict
#     reportrank : constr(min_length=1)
#     reporttype : constr(min_length=1)
#     state : list
#     summarizeby : constr(min_length=1)
#     usecode = {
#             "_uiSelectChoiceDisabled": bool,
#             "id": int,
#             "usecode": str,
#             "usecodegroup": str
#         }
#     year : list
#     zipcode : list

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
 
