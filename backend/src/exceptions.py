from typing import Type

from fastapi.responses import JSONResponse
from fastapi import status as statuscode
from pydantic import BaseModel

__all__ = (
    "BaseAPIException", "TickerNotFoundException",
    "SearchNotFoundException", "NetworkErrorException",
    "get_exception_responses"
)


class BaseError(BaseModel):
    message: str


class NotFoundError(BaseError):
    pass


class BaseAPIException(Exception):
    message = "Something went wrong"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}


class SearchNotFoundException(BaseAPIException):
    message = "Search Not Found"
    code = statuscode.HTTP_404_NOT_FOUND
    model = NotFoundError
    pass


class TickerNotFoundException(BaseAPIException):
    message = "Ticker not found"
    code = statuscode.HTTP_404_NOT_FOUND
    model = NotFoundError
    pass


class InternalServerErrorException(BaseAPIException):
    pass


class NetworkErrorException(BaseAPIException):
    pass


def get_exception_responses(*args: Type[BaseAPIException]) -> dict:
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
