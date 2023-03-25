import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class ReplyMessageBase(BaseSchema):
    message_type: Optional[str] = None
    message_text: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


class ReplyMessageCreate(ReplyMessageBase):
    event_id: int


class ReplyMessageUpdate(ReplyMessageBase):
    updated_at: datetime.datetime


class ReplyMessageResponse(ReplyMessageBase):
    id: int


class ReplyMessage(ReplyMessageBase):
    id: int

    class Config:
        orm_mode = True
