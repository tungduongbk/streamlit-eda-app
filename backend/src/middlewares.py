# # Installed # #
from fastapi import Request
from config import get_logger
from exceptions import BaseAPIException

__all__ = ("request_handler",)


logger = get_logger()


async def request_handler(request: Request, call_next):
    try:
        logger.debug(f"Received Request {request.method}|{request.url}")
        return await call_next(request)
    except Exception as ex:
        if isinstance(ex, BaseAPIException):
            return ex.response()

        raise ex
