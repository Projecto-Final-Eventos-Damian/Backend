from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/ticket-types",
    tags=["ticket-types"]
)

@router.post("/", response_model=schemas.TicketType, dependencies=[Depends(JWTBearer())])
def create(ticket_type: schemas.TicketTypeCreate, db: Session = Depends(get_db)):
    return crud.create_ticket_type(db, ticket_type)

@router.get("/", response_model=list[schemas.TicketType], dependencies=[Depends(JWTBearer())])
def get_all(db: Session = Depends(get_db)):
    return crud.get_all_ticket_types(db)

@router.get("/{ticket_type_id}", response_model=schemas.TicketType)
def get_by_id(ticket_type_id: int, db: Session = Depends(get_db)):
    ticket_type = crud.get_ticket_type_by_id(db, ticket_type_id)
    if not ticket_type:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    return ticket_type

@router.get("/event/{event_id}", response_model=list[schemas.TicketType])
def get_by_event(event_id: int, db: Session = Depends(get_db)):
    return crud.get_ticket_types_by_event(db, event_id)

@router.put("/{ticket_type_id}", response_model=schemas.TicketType, dependencies=[Depends(JWTBearer())])
def update(ticket_type_id: int, ticket_type_data: schemas.TicketTypeUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ticket_type(db, ticket_type_id, ticket_type_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    return updated

@router.delete("/{ticket_type_id}", response_model=schemas.TicketType, dependencies=[Depends(JWTBearer())])
def delete(ticket_type_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_ticket_type(db, ticket_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    return deleted
