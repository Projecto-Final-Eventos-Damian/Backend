from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(JWTBearer())]
)

# Crear una nueva categoría
@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

# Obtener todas las categorías
@router.get("/", response_model=list[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories

# Obtener una categoría por ID
@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Actualizar una categoría por ID
@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud.update_category(db=db, category_id=category_id, category=category)

# Eliminar una categoría por ID
@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud.delete_category(db=db, category_id=category_id)
