from pydantic import BaseModel, constr
from pydantic.types import constr, conint

##### LOAN ORIGINATOR MODULE (login, run_query, save_query, load_query) #####

class UsersSerializer(BaseModel):
    usr_username: constr(min_length=1)
    usr_email: str
    usr_password: str

class QuerySerializer(BaseModel):
    addgroup : str
    allowcustomregion : bool
    censustract : list
    citytown : list
    county : list
    customregion : bool
    lenderstodisplay : constr(min_length=1)
    lendertype : constr(min_length=1)
    loanmax : constr(min_length=1)
    loanmin : constr(min_length=1)
    loantypessubbypass : bool
    lt = {
             "lendertype": str ,
            "lendertypesetup": bool
        }
    nmlsid : constr(min_length=1)
    period : list
    pmmnonpmm : str
    refionly : bool
    reportformat : constr(min_length=1)
    reporting : dict
    reportrank : constr(min_length=1)
    reporttype : constr(min_length=1)
    state : list
    summarizeby : constr(min_length=1)
    usecode = {
            "_uiSelectChoiceDisabled": bool,
            "id": int,
            "usecode": str,
            "usecodegroup": str
        }
    year : list
    zipcode : list