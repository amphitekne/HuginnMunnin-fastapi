import logging
from HuginnMunnin_fastapi.exceptions import HuginnMuninnError, HuginnMuninnHTTPException
from fastapi import FastAPI, status

API_REF = 999

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MyError(HuginnMuninnError):
    api_ref = API_REF
    logger = logger


class InvalidOperationError(HuginnMuninnHTTPException):
    api_ref = API_REF
    status_code = status.HTTP_508_LOOP_DETECTED
    logger = logger


app = FastAPI()
# Exception handlers
app.add_exception_handler(**InvalidOperationError.fastapi_exception_handler())


@app.get("/works")
def get_gen():
    logger.info("This endpoint works")
    return {"message": "Welcome to FastAPI!"}


@app.get("/error/")
def get_gen():
    logger.info("This endpoint raises an error")
    raise MyError(
        interface_ref=1,
        generic_error_code=123,
        internal_error_code=432,
        detail="This is the detail of the error",
    )
    return {"message": "Welcome to FastAPI!"}


@app.get("/http-exception/")
def get_gen():
    logger.info("This endpoint raises an http exception")
    raise InvalidOperationError(
        interface_ref=1,
        generic_error_code=123,
        internal_error_code=432,
        detail="This is the detail of the error",
        user_message="Please, try again later.",
    )
    return {"message": "Welcome to FastAPI!"}


@app.get("/http-exception-2/")
def get_gen():
    logger.info("This endpoint raises an http exception")
    raise InvalidOperationError(
        internal_error_code=0,
        detail="This is the detail of the error",
        user_message="Please, try again later.",
    )
    return {"message": "Welcome to FastAPI!"}


@app.get("/overwriten-http-exception/")
def get_gen():
    logger.info("gen endpoint called")
    raise InvalidOperationError(
        status_code=status.HTTP_502_BAD_GATEWAY,
        interface_ref=1,
        generic_error_code=123,
        internal_error_code=432,
        detail="This is the detail of the error",
        user_message="Please, try again later.",
    )
    return {"message": "Welcome to FastAPI!"}
