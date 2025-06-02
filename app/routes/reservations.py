from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth.auth_bearer import JWTBearer
from app.utils.email import send_confirmation_email_with_attachment, render_email_template
from app.utils.pdf import generate_reservation_pdf
from app.utils.qr import generate_qr_base64
from app.utils.files import encode_image_to_base64, get_event_image_path

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)

# Crear una nueva reserva
@router.post("/", response_model=schemas.Reservation, dependencies=[Depends(JWTBearer())])
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    try:
        db_reservation = crud.create_reservation(db=db, reservation=reservation)
        return db_reservation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Enviar email de confirmacion de reserva con tickets
@router.post("/{reservation_id}/send-confirmation", dependencies=[Depends(JWTBearer())])
def send_reservation_confirmation(
    reservation_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_reservation = crud.get_reservation_by_id(db, reservation_id)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    user = db_reservation.user
    event = db_reservation.event
    tickets = crud.get_tickets_by_reservation_id(db, db_reservation.id)
    total_price = sum(ticket.ticket_type.price for ticket in tickets)
    logo_icon_path = get_event_image_path("public/images/logo/logo-icon.png")
    logo_text_path = get_event_image_path("public/images/logo/logo-text.png")

    for ticket in tickets:
        ticket.qr_base64 = generate_qr_base64(ticket.ticket_code)

    subject = f"Reserva confirmada para el evento {event.title}"

    html = render_email_template(
        "emails/reservation_conf.html",
        {
            "user_name": user.name,
            "event_title": event.title,
            "reservation_date": db_reservation.reserved_at.strftime('%d/%m/%Y'),
            "reservation_id": db_reservation.id,
            "total_price": total_price
        }
    )

    pdf_bytes = generate_reservation_pdf({
        "user_name": user.name,
        "reservation_date": db_reservation.reserved_at.strftime('%d/%m/%Y'),
        "reservation_id": db_reservation.id,
        "tickets": tickets,
        "logo_icon_base64": encode_image_to_base64(logo_icon_path),
        "logo_text_base64": encode_image_to_base64(logo_text_path),
        "event": {
            "title": event.title,
            "image_url": event.image_url,
            "start_date": event.start_date_time.strftime('%d/%m/%Y - %H:%M'),
            "end_date": event.end_date_time.strftime('%d/%m/%Y - %H:%M'),
            "location": event.location
        }
    })

    background_tasks.add_task(
        send_confirmation_email_with_attachment,
        user.email,
        subject,
        html,
        pdf_bytes,
        f"tickets_reserva_{db_reservation.id}.pdf"
    )

    return {"message": "Confirmation email sent."}

# Actualizar una reserva
@router.put("/{reservation_id}", response_model=schemas.Reservation, dependencies=[Depends(JWTBearer())])
def update_reservation(reservation_id: int, reservation: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = crud.update_reservation(db=db, reservation_id=reservation_id, reservation=reservation)
    if db_reservation:
        return db_reservation
    raise HTTPException(status_code=404, detail="Reservation not found")

# Eliminar una reserva
@router.delete("/{reservation_id}", response_model=schemas.Reservation, dependencies=[Depends(JWTBearer())])
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    user = db_reservation.user
    event = db_reservation.event
    db.delete(db_reservation)
    db.commit()
    reservation_data = schemas.Reservation.from_orm(db_reservation)
    reservation_data.user = schemas.User.from_orm(user)
    reservation_data.event = schemas.Event.from_orm(event)
    return reservation_data

# Obtener todas las reservas
@router.get("/", response_model=list[schemas.Reservation], dependencies=[Depends(JWTBearer())])
def get_all_reservations(db: Session = Depends(get_db)):
    db_reservations = crud.get_all_reservations(db=db)
    return db_reservations

# Obtener reservas por user Id con sus tiquets
@router.get("/user/{user_id}/tickets", response_model=list[schemas.ReservationWithTickets], dependencies=[Depends(JWTBearer())])
def get_user_reservations_with_tickets(user_id: int, db: Session = Depends(get_db)):
    db_reservations = crud.get_reservations_by_user(db, user_id)
    result = []
    for reservation in db_reservations:
        tickets = crud.get_tickets_by_reservation_id(db, reservation.id)
        result.append({
            "reservation": reservation,
            "tickets": tickets
        })
    return result

# Obtener reservas por event Id con sus tiquets
@router.get("/event/{event_id}/tickets", response_model=list[schemas.ReservationWithTickets], dependencies=[Depends(JWTBearer())])
def get_event_reservations_with_tickets(event_id: int, db: Session = Depends(get_db)):
    db_reservations = crud.get_reservations_by_event(db, event_id)
    result = []
    for reservation in db_reservations:
        tickets = crud.get_tickets_by_reservation_id(db, reservation.id)
        result.append({
            "reservation": reservation,
            "tickets": tickets
        })
    return result

# Obtener una reserva por su ID
@router.get("/{reservation_id}", response_model=schemas.Reservation, dependencies=[Depends(JWTBearer())])
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crud.get_reservation_by_id(db=db, reservation_id=reservation_id)
    if db_reservation:
        return db_reservation
    raise HTTPException(status_code=404, detail="Reservation not found")

# Obtener todas las reservas de un usuario
@router.get("/user/{user_id}", response_model=list[schemas.Reservation], dependencies=[Depends(JWTBearer())])
def get_reservations_by_user(user_id: int, db: Session = Depends(get_db)):
    db_reservations = crud.get_reservations_by_user(db=db, user_id=user_id)
    return db_reservations

# Obtener todas las reservas de un evento
@router.get("/event/{event_id}", response_model=list[schemas.Reservation], dependencies=[Depends(JWTBearer())])
def get_reservations_by_event(event_id: int, db: Session = Depends(get_db)):
    db_reservations = crud.get_reservations_by_event(db=db, event_id=event_id)
    return db_reservations

# Obtener numero de tiquets reservados
@router.get("/event/{event_id}/reserved-count", response_model=int)
def get_reserved_tickets_count(event_id: int, db: Session = Depends(get_db)):
    return crud.get_reserved_tickets_count(db, event_id)