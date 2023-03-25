import os
import sys
from functools import lru_cache

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    APP_NAME: str = "Chatgpt Line Bot"
    APP_VERSION: str = "v1"


class LocalConfig(BaseConfig):
    DEBUG: bool = True
    DATABASE_URL: str = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DATABASE')}?charset=utf8mb4"


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    DATABASE_URL: str = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DATABASE')}?charset=utf8mb4"


class IntegrationConfig(BaseConfig):
    DEBUG: bool = False


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    DATABASE_URL: str = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@/{os.getenv('MYSQL_DATABASE')}?unix_socket=/cloudsql/{os.getenv('MYSQL_HOST')}&charset=utf8mb4"


@lru_cache(maxsize=0 if "pytest" in sys.modules else 256)
def get_base_config() -> BaseSettings:
    if os.getenv("BUILD_ENV") == "production":
        return ProductionConfig()
    elif os.getenv("BUILD_ENV") == "integration":
        return IntegrationConfig()
    elif os.getenv("BUILD_ENV") == "testing":
        return LocalConfig()
    else:
        return DevelopmentConfig()
