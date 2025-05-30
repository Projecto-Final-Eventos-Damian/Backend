import bcrypt
from sqlalchemy.orm import Session
from app import models, schemas

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        name=user.name, 
        email=user.email, 
        password_hash=hashed_password, 
        role=user.role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users_with_reservations(db: Session, event_id: int):
    return db.query(models.User).join(models.Reservation).filter(models.Reservation.event_id == event_id).all()

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        if user.password:
            db_user.password_hash = hash_password(user.password)
        db_user.role = user.role.value
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
