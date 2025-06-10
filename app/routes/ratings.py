from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer
from datetime import datetime

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
    dependencies=[Depends(JWTBearer())]
)

# Crear una nueva valoración
@router.post("/", response_model=schemas.EventRating)
def create_rating(rating: schemas.EventRatingCreate, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == rating.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="El evento no existe")

    if datetime.now() < event.end_date_time:
        raise HTTPException(status_code=403, detail="No puedes valorar un evento que aún no ha finalizado")

    if event.organizer_id == rating.user_id:
        raise HTTPException(status_code=403, detail="No puedes valorar tu propio evento")

    reservation = db.query(models.Reservation).filter_by(
        user_id=rating.user_id,
        event_id=rating.event_id
    ).first()
    if not reservation:
        raise HTTPException(status_code=403, detail="Debes tener una reserva para valorar este evento")

    try:
        new_rating = crud.create_rating(db=db, rating=rating)
        return new_rating
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Ya has valorado este evento anteriormente."
        )

# Obtener todas las valoraciones
@router.get("/", response_model=list[schemas.EventRating])
def get_ratings(db: Session = Depends(get_db)):
    return crud.get_ratings(db=db)

# Obtener valoración por ID
@router.get("/{rating_id}", response_model=schemas.EventRating)
def get_rating_by_id(rating_id: int, db: Session = Depends(get_db)):
    rating = crud.get_rating_by_id(db=db, rating_id=rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

# Actualizar valoración
@router.put("/{rating_id}", response_model=schemas.EventRating)
def update_rating(rating_id: int, rating: schemas.EventRatingUpdate, db: Session = Depends(get_db)):
    updated_rating = crud.update_rating(db=db, rating_id=rating_id, rating=rating)
    if not updated_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return updated_rating

# Eliminar valoración
@router.delete("/{rating_id}", response_model=schemas.EventRating)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(models.EventRating).filter(models.EventRating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    user = rating.user
    event = rating.event
    db.delete(rating)
    db.commit()
    rating_data = schemas.EventRating.from_orm(rating)
    rating_data.user = schemas.User.from_orm(user)
    rating_data.event = schemas.Event.from_orm(event)
    return rating_data

# Obtener valoraciones por usuario
@router.get("/user/{user_id}", response_model=list[schemas.EventRating])
def get_ratings_by_user(user_id: int, db: Session = Depends(get_db)):
    ratings = crud.get_ratings_by_user(db=db, user_id=user_id)
    return ratings

# Obtener valoraciones por evento
@router.get("/event/{event_id}", response_model=list[schemas.EventRating])
def get_ratings_by_event(event_id: int, db: Session = Depends(get_db)):
    ratings = crud.get_ratings_by_event(db=db, event_id=event_id)
    return ratings
