from sqlalchemy.orm import Session
from app import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    # Hasheamos la contraseña (reemplazar esto con un proceso real de hash)
    hashed_password = user.password  # Aquí deberías hashear la contraseña
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

def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.password_hash = user.password  # Aquí deberías encriptar la contraseña
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