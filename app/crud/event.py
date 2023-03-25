from sqlalchemy.orm import Session

from app import models, schemas


def get_event(db: Session, id: int) -> models.Event:
    return db.query(models.Event).filter(models.Event.id == id).first()


def get_events_by_user_id(
    db: Session, user_id: str, limit: int = 4
) -> list[models.Event]:
    return (
        db.query(models.Event)
        .filter(models.Event.user_id == user_id)
        .offset(0)
        .limit(limit)
        .order_by(models.Event.timestamp.desc())
        .all()
    )


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    data = models.Event(**event.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def create_event_by_line(db: Session, event: any) -> models.Event:
    db_event = schemas.EventCreate(
        type=event.type,
        mode=event.mode,
        reply_token=event.reply_token,
        web_hook_event_id=event.webhook_event_id,
        timestamp=event.timestamp,
        source_type=event.source.type,
        user_id=event.source.user_id,
        message_type=event.message.type,
        message_id=event.message.id,
        message_text=event.message.text,
    )

    data = create_event(db=db, event=db_event)
    return data
