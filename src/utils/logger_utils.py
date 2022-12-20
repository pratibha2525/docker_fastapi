import logging
from sqlalchemy import null

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class LoggerUtil():

    @classmethod
    def info(cls,message):
        builder = " Info message: "+message
        if(builder!=null):
            logger.info(builder)

    @classmethod
    def debug(cls,message,value):
        builder = " Debug message: "+ str(message)+ " Debug value: "+ str(value)
        if(builder!=null) :
            logger.debug(builder)

    @classmethod
    def error(cls,message):

        builder = "Error message: "+message
        if(builder!=null):
            logger.error(builder)

    @classmethod
    def logException(cls,method_name, exception=None, var_args = None) :

            if (exception != null) :
                builder = "***Exception message: "+ exception

            if (var_args != null) :
                builder = builder + "***Object's state when exception occured :"
                builder +="***Message for ***"+method_name + "()"

            if(builder!=null) :
                logger.error(builder, exception)

            logger.error(builder)
