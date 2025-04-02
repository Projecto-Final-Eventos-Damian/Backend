from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

# Esquema para los diferentes roles de los usuarios
class UserRole(str, Enum):
    user = "user"
    organizer = "organizer"
    admin = "admin"

# Esquema para la creación de un nuevo usuario
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user  # Por defecto, el rol es "user"

# Esquema para el usuario en las respuestas (como la información que se devuelve)
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True  # Esto permite que el modelo ORM de SQLAlchemy sea convertido a dict para respuestas
