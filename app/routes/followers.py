from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/followers",
    tags=["followers"]
)

# Seguir a un organizador
@router.post("/", response_model=schemas.UserFollower, dependencies=[Depends(JWTBearer())])
def follow_organizer(follower: schemas.UserFollowerCreate, db: Session = Depends(get_db)):
    try:
        new_follow = crud.follow_organizer(db, follower.user_id, follower.organizer_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not new_follow:
        raise HTTPException(status_code=400, detail="El usuario seguido no es un organizador")
    return new_follow

# Obtener los seguidores de un organizador (mostrar los usuarios que siguen a un organizador)
@router.get("/organizer/{organizer_id}", response_model=list[schemas.User])
def get_followers(organizer_id: int, db: Session = Depends(get_db)):
    followers = crud.get_followers(db, organizer_id)
    return followers

# Obtener a quién sigue un usuario (mostrar los organizadores que un usuario sigue)
@router.get("/user/{user_id}", response_model=list[schemas.User])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = crud.get_following(db, user_id)
    return following

# Dejar de seguir a un organizador
@router.delete("/{user_id}/{organizer_id}", response_model=schemas.UserFollower, dependencies=[Depends(JWTBearer())])
def unfollow_organizer(user_id: int, organizer_id: int, db: Session = Depends(get_db)):
    follower = db.query(models.UserFollower).filter(
        models.UserFollower.user_id == user_id,
        models.UserFollower.organizer_id == organizer_id
    ).first()
    if not follower:
        raise HTTPException(status_code=404, detail="No se encontró la relación de seguimiento")
    user = follower.user
    organizer = follower.organizer
    db.delete(follower)
    db.commit()
    follower_data = schemas.UserFollower.from_orm(follower)
    follower_data.user = schemas.User.from_orm(user)
    follower_data.organizer = schemas.User.from_orm(organizer)
    return follower_data

# Ver todas las relaciones de seguimiento
@router.get("/", response_model=list[schemas.UserFollower], dependencies=[Depends(JWTBearer())])
def get_all_user_followers(db: Session = Depends(get_db)):
    return crud.get_all_user_followers(db)

# Comprobar seguimiento de usuarios
@router.get("/check/{user_id}/{organizer_id}")
def check_follow(user_id: int, organizer_id: int, db: Session = Depends(get_db)):
    follow = db.query(models.UserFollower).filter_by(
        user_id=user_id,
        organizer_id=organizer_id
    ).first()
    return {"is_following": bool(follow)}