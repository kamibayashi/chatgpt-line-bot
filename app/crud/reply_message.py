from sqlalchemy.orm import Session

from app import models, schemas


def get_reply_message(db: Session, id: int) -> models.ReplyMessage:
    return db.query(models.ReplyMessage).filter(models.ReplyMessage.id == id).first()


def get_reply_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ReplyMessage).offset(skip).limit(limit).all()


def create_reply_message(
    db: Session, reply: schemas.ReplyMessageCreate
) -> models.ReplyMessage:
    data = models.ReplyMessage(**reply.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def create_reply_message_by_chatgpt(
    db: Session, event: models.Event, reply: any
) -> models.ReplyMessage:
    db_reply = schemas.ReplyMessageCreate(
        event_id=event.id,
        message_type=event.message_type,
        message_text=reply,
    )

    data = create_reply_message(db=db, reply=db_reply)
    return data
