import pydantic
import logging

__all__ = ("api_settings", "get_logger", )


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = "sample.env"


class APISettings(BaseSettings):
    title: str = "Company Stock API"
    host: str = "0.0.0.0"
    port: int = 8083
    log_level: str = "INFO"

    class Config(BaseSettings.Config):
        env_prefix = "API_"


api_settings = APISettings()

logging.basicConfig(
    level=api_settings.log_level,
    format="""%(asctime)s.%(msecs)d %(levelname)-8s[%(filename)s:%(funcName)s:%(lineno)d] %(message)s""",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def get_logger(level="INFO"):
    MSG_FORMAT = "%(asctime)s.%(msecs)d %(levelname)-8s[%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(format=MSG_FORMAT, datefmt=DATETIME_FORMAT)
    logger = logging.getLogger(__name__)
    if level == "INFO":
        logger.setLevel(logging.INFO)
    elif level == "WARNING":
        logger.setLevel(logging.WARNING)
    elif level == "ERROR":
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.DEBUG)

    return logger
