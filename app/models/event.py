from sqlalchemy import BigInteger, Column, Float, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base

from . import BaseModel


class Event(Base, BaseModel):
    __tablename__ = "events"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    type = Column(String(32), index=True, nullable=False)
    mode = Column(String(32), index=True)
    source_type = Column(String(32), index=True)
    user_id = Column(String(64), index=True)
    web_hook_event_id = Column(String(255), index=True)
    reply_token = Column(String(255), index=True)
    message_id = Column(String(255), index=True, nullable=False)
    message_type = Column(String(32), index=True)
    message_text = Column(Text)
    timestamp = Column(Float)

    reply_messages = relationship("ReplyMessage", back_populates="event")
