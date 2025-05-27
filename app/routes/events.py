from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_dependencies import RoleChecker
from datetime import datetime
import os, uuid, shutil
from typing import List

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# Listar todos los eventos
@router.get("/", response_model=list[schemas.Event])
def get_events(db: Session = Depends(get_db)):
    return crud.get_events(db=db)


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Crear un nuevo evento
@router.post("/", response_model=schemas.Event, dependencies=[Depends(RoleChecker(["organizer"]))])
def create_event(
    title: str = Form(...),
    description: str = Form(None),
    category_id: int = Form(...),
    organizer_id: int = Form(...),
    capacity: int = Form(...),
    start_date_time: datetime = Form(...),
    end_date_time: datetime = Form(...),
    location: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()

    if start_date_time < now:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio no puede ser anterior a la fecha/hora actual"
        )

    if end_date_time <= start_date_time:
        raise HTTPException(
            status_code=400,
            detail="La fecha de finalización debe ser posterior a la fecha/hora de inicio"
        )

    image_url = None

    if image:
        if not allowed_file(image.filename):
            raise HTTPException(
                status_code=400,
                detail="El archivo debe ser una imagen con extensión .jpg, .jpeg o .png"
            )

        image_folder = "public/images/events"
        os.makedirs(image_folder, exist_ok=True)

        ext = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        image_path = os.path.join(image_folder, unique_filename)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = f"/{image_path}"

    new_event = crud.create_event(
        db=db,
        event=schemas.EventCreate(
            title=title,
            description=description,
            category_id=category_id,
            organizer_id=organizer_id,
            capacity=capacity,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            location=location,
            image_url=image_url
        )
    )

    if not new_event:
        raise HTTPException(
            status_code=404,
            detail="No se pudo crear el evento"
        )

    return new_event

# Obtener un evento por ID
@router.get("/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event_by_id(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

# Obtener todos los eventos de un organizador
@router.get("/organizer/{organizer_id}", response_model=List[schemas.Event])
def get_events_by_organizer(organizer_id: int, db: Session = Depends(get_db)):
    events = crud.get_events_by_organizer(db, organizer_id)
    if not events:
        raise HTTPException(status_code=404, detail="No se encontraron eventos para este organizador")
    return events

# Editar un evento por Id
@router.put("/{event_id}", response_model=schemas.Event, dependencies=[Depends(RoleChecker(["organizer"]))])
def update_event(
    event_id: int,
    title: str = Form(...),
    description: str = Form(None),
    category_id: int = Form(...),
    organizer_id: int = Form(...),
    capacity: int = Form(...),
    start_date_time: datetime = Form(...),
    end_date_time: datetime = Form(...),
    location: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_event = crud.get_event_by_id(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    now = datetime.utcnow()

    if end_date_time <= start_date_time:
        raise HTTPException(
            status_code=400,
            detail="La fecha de finalización debe ser posterior a la fecha/hora de inicio"
        )

    image_url = db_event.image_url

    if image:
        if not allowed_file(image.filename):
            raise HTTPException(
                status_code=400,
                detail="El archivo debe ser una imagen con extensión .jpg, .jpeg o .png"
            )

        if db_event.image_url:
            old_image_path = db_event.image_url.lstrip("/")
            if os.path.exists(old_image_path):
                try:
                    os.remove(old_image_path)
                except Exception as e:
                    print(f"No se pudo eliminar la imagen anterior: {e}")

        image_folder = "public/images/events"
        os.makedirs(image_folder, exist_ok=True)

        ext = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        image_path = os.path.join(image_folder, unique_filename)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = f"/{image_path}"

    updated_event = crud.update_event(
        db=db,
        event_id=event_id,
        event=schemas.EventCreate(
            title=title,
            description=description,
            category_id=category_id,
            organizer_id=organizer_id,
            capacity=capacity,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            location=location,
            image_url=image_url
        )
    )

    return updated_event

# Eliminar un evento por ID
@router.delete("/{event_id}", response_model=schemas.Event, dependencies=[Depends(RoleChecker(["organizer"]))])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event_by_id(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event_data = schemas.Event.model_validate(db_event)  
    crud.delete_event(db=db, event_id=event_id)
    return event_data