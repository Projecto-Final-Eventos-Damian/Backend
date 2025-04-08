import random
from sqlalchemy.orm import Session
from app import models, schemas

def generate_unique_ticket_code(db: Session) -> str:
    while True:
        code = str(random.randint(10**12, (10**13) - 1))  # 13-digit number
        exists = db.query(models.Ticket).filter(models.Ticket.ticket_code == code).first()
        if not exists:
            return code

def create_ticket(db: Session, ticket: schemas.TicketCreate) -> models.Ticket:
    code = generate_unique_ticket_code(db)
    db_ticket = models.Ticket(
        reservation_id=ticket.reservation_id,
        ticket_code=code,
        price=ticket.price
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def get_all_tickets(db: Session):
    return db.query(models.Ticket).all()

def update_ticket(db: Session, ticket_id: int, status: str):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if ticket:
        ticket.status = status
        db.commit()
        db.refresh(ticket)
    return ticket

def delete_ticket(db: Session, ticket_id: int):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if ticket:
        db.delete(ticket)
        db.commit()
        return ticket
    return None
