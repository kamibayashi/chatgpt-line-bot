from typing import Any

from sqlalchemy import Column, DateTime, Integer, event, func, orm
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp

from app.core.logger import get_logger

logger = get_logger(__name__)


class BaseModel:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=current_timestamp(),
        onupdate=func.utc_timestamp(),
    )
    deleted_at = Column(DateTime)


@event.listens_for(Session, "do_orm_execute")
def _add_filtering_deleted_at(execute_state: Any) -> None:
    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                BaseModel,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )
