from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

Base = declarative_base()

try:
    engine = create_engine(
        settings.BASE_CONFIG.DATABASE_URL,
        connect_args={"auth_plugin": "mysql_native_password"},
        pool_pre_ping=True,
    )
    logger.info(engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"DB connection error. detail={e}")


def get_db() -> Generator:
    db = None
    try:
        db = session_factory()
        yield db
        db.commit()
    except Exception:
        if db:
            db.rollback()
    finally:
        if db:
            db.close()
