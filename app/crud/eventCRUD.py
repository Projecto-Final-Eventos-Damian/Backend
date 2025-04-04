from sqlalchemy.orm import Session
from app import models, schemas

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(
        title=event.title,
        description=event.description,
        category_id=event.category_id,
        organizer_id=event.organizer_id,
        capacity=event.capacity,
        start_date_time=event.start_date_time,
        end_date_time=event.end_date_time,
        location=event.location,
        image_url=str(event.image_url) if event.image_url else None
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session):
    return db.query(models.Event).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db_event.title = event.title
        db_event.description = event.description
        db_event.category_id = event.category_id
        db_event.organizer_id = event.organizer_id
        db_event.capacity = event.capacity
        db_event.start_date_time = event.start_date_time
        db_event.end_date_time = event.end_date_time
        db_event.location = event.location
        db_event.image_url = str(event.image_url) if event.image_url else None
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event
