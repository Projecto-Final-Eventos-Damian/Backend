from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import IntegrityError

def follow_organizer(db: Session, user_id: int, organizer_id: int):
    if user_id == organizer_id:
        raise ValueError("No puedes seguirte a ti mismo")

    organizer = db.query(models.User).filter(
        models.User.id == organizer_id,
        models.User.role == "organizer"
    ).first()

    if not organizer:
        return None

    follower = models.UserFollower(user_id=user_id, organizer_id=organizer_id)
    db.add(follower)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya estás siguiendo a este organizador")

    db.refresh(follower)
    return follower

def get_followers(db: Session, organizer_id: int):
    # Obtenemos los seguidores de un organizador. Queremos los usuarios que siguen a ese organizador.
    followers = db.query(models.User).join(
            models.UserFollower, 
            models.UserFollower.user_id == models.User.id
        ).filter(models.UserFollower.organizer_id == organizer_id).all()
    return followers

def get_following(db: Session, user_id: int):
    # Obtenemos los organizadores que un usuario sigue. Queremos los organizadores que son seguidos por ese usuario.
    following = db.query(models.User).join(
            models.UserFollower, 
            models.UserFollower.organizer_id == models.User.id
        ).filter(models.UserFollower.user_id == user_id).all()
    return following

def unfollow_organizer(db: Session, user_id: int, organizer_id: int):
    follower = db.query(models.UserFollower).filter(models.UserFollower.user_id == user_id, models.UserFollower.organizer_id == organizer_id).first()
    if follower:
        db.delete(follower)
        db.commit()
    return follower

def get_all_user_followers(db: Session):
    return db.query(models.UserFollower).all()