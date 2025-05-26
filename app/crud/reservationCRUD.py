from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app import models, schemas

def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    event = db.query(models.Event).filter(models.Event.id == reservation.event_id).first()
    if not event:
        raise ValueError("El evento no existe.")

    total_reserved = db.query(func.sum(models.Reservation.tickets_number))\
        .filter(models.Reservation.event_id == reservation.event_id)\
        .filter(models.Reservation.status != "cancelled")\
        .scalar() or 0

    if total_reserved + reservation.tickets_number > event.capacity:
        raise ValueError("No hay suficientes plazas disponibles para este evento.")

    db_reservation = models.Reservation(
        user_id=reservation.user_id,
        event_id=reservation.event_id,
        status=reservation.status,
        tickets_number=reservation.tickets_number
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_all_reservations(db: Session):
    return db.query(models.Reservation).all()

def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def get_reservations_by_user(db: Session, user_id: int):
    return db.query(models.Reservation).filter(models.Reservation.user_id == user_id).all()

def get_reservations_by_event(db: Session, event_id: int):
    return db.query(models.Reservation).filter(models.Reservation.event_id == event_id).all()

def get_reserved_tickets_count(db: Session, event_id: int) -> int:
    return db.query(func.coalesce(func.sum(models.Reservation.tickets_number), 0))\
        .filter(models.Reservation.event_id == event_id)\
        .filter(models.Reservation.status != "cancelled")\
        .scalar()

def update_reservation(db: Session, reservation_id: int, reservation: schemas.ReservationUpdate):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if db_reservation:
        db_reservation.status = reservation.status
        db.commit()
        db.refresh(db_reservation)
        return db_reservation
    return None

def delete_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
        return db_reservation
    return None
