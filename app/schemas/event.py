import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class EventBase(BaseSchema):
    type: Optional[str] = None
    mode: Optional[str] = None
    source_type: Optional[str] = None
    user_id: Optional[str] = None
    web_hook_event_id: Optional[str] = None
    reply_token: Optional[str] = None
    message_id: Optional[str] = None
    message_type: Optional[str] = None
    message_text: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


class EventCreate(EventBase):
    type: str
    mode: str
    source_type: str
    user_id: str
    timestamp: float


class EventUpdate(EventBase):
    updated_at: datetime.datetime


class EventResponse(EventBase):
    id: int
    name: str


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True
