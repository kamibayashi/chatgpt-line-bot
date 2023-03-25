from sqlalchemy import BigInteger, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base

from . import BaseModel


class ReplyMessage(Base, BaseModel):
    __tablename__ = "reply_messages"
    mysql_charset = ("utf8mb4",)
    mysql_collate = "utf8mb4_unicode_ci"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey("events.id"), index=True, nullable=False)
    message_type = Column(String(32), nullable=False)
    message_text = Column(Text)

    event = relationship("Event", back_populates="reply_messages")
