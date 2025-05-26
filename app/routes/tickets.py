from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
    dependencies=[Depends(JWTBearer())]
)

@router.post("/", response_model=schemas.Ticket)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(db, ticket)

@router.get("/", response_model=list[schemas.Ticket])
def get_all_tickets(db: Session = Depends(get_db)):
    return crud.get_all_tickets(db)

@router.get("/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = crud.get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/reservation/{reservation_id}", response_model=list[schemas.Ticket])
def get_tickets_by_reservation_id(reservation_id: int, db: Session = Depends(get_db)):
    tickets = crud.get_tickets_by_reservation_id(db, reservation_id)
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found for this reservation")
    return tickets

@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(ticket_id: int, status: schemas.TicketUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ticket(db, ticket_id, status.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated

@router.delete("/{ticket_id}", response_model=schemas.Ticket)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    reservation_exists = db.query(models.Reservation).filter(models.Reservation.id == ticket.reservation_id).first()
    if reservation_exists:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el ticket porque la reserva asociada aún existe"
        )
    ticket_data = schemas.Ticket.from_orm(ticket)
    db.delete(ticket)
    db.commit()
    return ticket_data
