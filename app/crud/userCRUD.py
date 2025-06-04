import bcrypt, os, shutil, uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app import models, schemas

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png"]
DEFAULT_IMAGE_PATH = "public/images/users/default.png"

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

def update_user_partial(db, user_id: int, name=None, email=None, image: UploadFile = None):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    if name:
        user.name = name
    if email:
        user.email = email

    if image:
        ext = os.path.splitext(image.filename)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError("El archivo debe ser una imagen .jpg, .jpeg o .png")

        if user.image_url and user.image_url != DEFAULT_IMAGE_PATH:
            old_image_path = user.image_url.lstrip("/")
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except Exception as e:
                    print(f"No se pudo eliminar la imagen anterior: {e}")

        image_folder = "public/images/users"
        os.makedirs(image_folder, exist_ok=True)

        unique_filename = f"{uuid.uuid4().hex}{ext}"
        image_path = os.path.join(image_folder, unique_filename)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        user.image_url = f"/{image_path}"

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if db_user.image_url and db_user.image_url != DEFAULT_IMAGE_PATH:
            image_path = db_user.image_url.lstrip("/")
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"No se pudo eliminar la imagen: {e}")

        db.delete(db_user)
        db.commit()
    return db_user

def delete_user_image(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    if user.image_url and user.image_url != None:
        image_path = user.image_url.lstrip("/")
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"No se pudo eliminar la imagen: {e}")
    
    user.image_url = None
    db.commit()
    db.refresh(user)
    return user