from datetime import datetime
from sqlalchemy.orm import Session
from app import crud
from app.utils.email import render_email_template
from email.message import EmailMessage
import smtplib
import os

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

def send_rating_emails(db: Session, base_frontend_url: str):
    reservations = crud.get_all_reservations(db)

    for reservation in reservations:
        event = reservation.event
        if event.end_date_time <= datetime.now() and not reservation.rating_sent:
            user = reservation.user

            rating_url = f"{base_frontend_url}/encuesta/{reservation.id}"

            html = render_email_template(
                "emails/event_rating.html",
                {
                    "user_name": user.name,
                    "event_title": event.title,
                    "rating_url": rating_url
                }
            )

            msg = EmailMessage()
            msg["Subject"] = f"Valora el evento {event.title}"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = user.email
            msg.add_alternative(html, subtype="html")

            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

            reservation.rating_sent = True
            db.add(reservation)

    db.commit()