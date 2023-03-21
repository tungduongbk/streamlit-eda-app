# # Installed # #
from fastapi import Request

__all__ = ("request_handler",)

from src.exceptions import BaseAPIException
from src.config import get_logger

logger = get_logger()


async def request_handler(request: Request, call_next):
    try:
        logger.debug(f"Received Request {request.method}|{request.url}")
        return await call_next(request)
    except Exception as ex:
        if isinstance(ex, BaseAPIException):
            return ex.response()

        raise ex

