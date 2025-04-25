from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

# Listar todos los eventos
@router.get("/", response_model=list[schemas.Event])
def get_events(db: Session = Depends(get_db)):
    return crud.get_events(db=db)

# Crear un nuevo evento
@router.post("/", response_model=schemas.Event, dependencies=[Depends(JWTBearer())])
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    new_event = crud.create_event(db=db, event=event)
    if not new_event:
        raise HTTPException(
            status_code=400, 
            detail="Solo los usuarios con rol de organizador pueden crear eventos"
        )
    return new_event

# Obtener un evento por ID
@router.get("/{event_id}", response_model=schemas.Event, dependencies=[Depends(JWTBearer())])
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event_by_id(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

# Actualizar un evento por ID
@router.put("/{event_id}", response_model=schemas.Event, dependencies=[Depends(JWTBearer())])
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = crud.get_event_by_id(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return crud.update_event(db=db, event_id=event_id, event=event)

# Eliminar un evento por ID
@router.delete("/{event_id}", response_model=schemas.Event, dependencies=[Depends(JWTBearer())])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event_by_id(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event_data = schemas.Event.model_validate(db_event)  
    crud.delete_event(db=db, event_id=event_id)
    return event_data