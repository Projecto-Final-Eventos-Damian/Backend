from sqlalchemy.orm import Session
from app import models, schemas

def create_rating(db: Session, rating: schemas.EventRatingCreate):
    db_rating = models.EventRating(
        user_id=rating.user_id,
        event_id=rating.event_id,
        rating=rating.rating,
        review=rating.review
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings(db: Session):
    return db.query(models.EventRating).all()

def get_rating_by_id(db: Session, rating_id: int):
    return db.query(models.EventRating).filter(models.EventRating.id == rating_id).first()

def update_rating(db: Session, rating_id: int, rating: schemas.EventRatingUpdate):
    db_rating = db.query(models.EventRating).filter(models.EventRating.id == rating_id).first()
    if db_rating:
        db_rating.rating = rating.rating
        db_rating.review = rating.review
        db.commit()
        db.refresh(db_rating)
    return db_rating

def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(models.EventRating).filter(models.EventRating.id == rating_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()
    return db_rating

def get_ratings_by_user(db: Session, user_id: int):
    return db.query(models.EventRating).filter(models.EventRating.user_id == user_id).all()

def get_ratings_by_event(db: Session, event_id: int):
    return db.query(models.EventRating).filter(models.EventRating.event_id == event_id).all()
