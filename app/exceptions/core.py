from fastapi import HTTPException


class ApplicationError(HTTPException):
    pass
