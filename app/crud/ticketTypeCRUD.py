from sqlalchemy.orm import Session
from app import models, schemas

def create_ticket_type(db: Session, ticket_type: schemas.TicketTypeCreate):
    db_ticket_type = models.TicketType(**ticket_type.dict())
    db.add(db_ticket_type)
    db.commit()
    db.refresh(db_ticket_type)
    return db_ticket_type

def get_all_ticket_types(db: Session):
    return db.query(models.TicketType).all()

def get_ticket_type_by_id(db: Session, ticket_type_id: int):
    return db.query(models.TicketType).filter(models.TicketType.id == ticket_type_id).first()

def get_ticket_types_by_event(db: Session, event_id: int):
    return db.query(models.TicketType).filter(models.TicketType.event_id == event_id).all()

def update_ticket_type(db: Session, ticket_type_id: int, ticket_type_data: schemas.TicketTypeUpdate):
    db_ticket_type = get_ticket_type_by_id(db, ticket_type_id)
    if db_ticket_type:
        for field, value in ticket_type_data.dict(exclude_unset=True).items():
            setattr(db_ticket_type, field, value)
        db.commit()
        db.refresh(db_ticket_type)
    return db_ticket_type

def delete_ticket_type(db: Session, ticket_type_id: int):
    db_ticket_type = get_ticket_type_by_id(db, ticket_type_id)
    if db_ticket_type:
        db.delete(db_ticket_type)
        db.commit()
    return db_ticket_type
