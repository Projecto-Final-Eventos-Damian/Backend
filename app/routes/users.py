from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(JWTBearer())]
)

# Crear un nuevo usuario
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# Obtener todos los usuarios
@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

# Obtener un usuario por ID
@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Actualizar un usuario por ID
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

# Actualizar un usuario parcialmente por ID
@router.patch("/{user_id}", response_model=schemas.User)
def update_user_partial(
    user_id: int,
    name: str = Form(None),
    email: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.update_user_partial(
        db=db,
        user_id=user_id,
        name=name,
        email=email,
        image=image
    )

# Eliminar un usuario por ID
@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.delete_user(db=db, user_id=user_id)


@router.delete("/{user_id}/image", response_model=schemas.User)
def delete_user_image(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.delete_user_image(db=db, user_id=user_id)