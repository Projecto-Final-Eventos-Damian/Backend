from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None  # Descripción es opcional

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # Permite convertir los modelos de SQLAlchemy a Pydantic
