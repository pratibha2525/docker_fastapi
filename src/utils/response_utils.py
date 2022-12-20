from fastapi import status
from fastapi.responses import JSONResponse

class ResponseUtil:

    @classmethod
    def success_response(cls,data = None,message="Success",status_code=status.HTTP_200_OK):
        if data == None:
            return JSONResponse({
            "status_code" : status_code,
            "message":message,
        })

        return JSONResponse({
            "status_code" : status_code,
            "message":message,
            "data":data
        })

    @classmethod
    def error_response(cls,message="Error",status_code=status.HTTP_400_BAD_REQUEST):
        return JSONResponse({
            "response_code":status_code,
            "message":message
        })
