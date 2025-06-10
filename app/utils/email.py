import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), cache_size=0)

def render_email_template(template_name: str, context: dict) -> str:
    template = jinja_env.get_template(template_name)
    return template.render(context)

def send_confirmation_email_with_attachment(to_email, subject, html_content, pdf_bytes, filename):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    msg.add_alternative(html_content, subtype="html")

    msg.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=filename
    )

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def send_rating_emails(db: Session, base_frontend_url: str):
    reservations = crud.get_all_reservations(db)

    for reservation in reservations:
        event = reservation.event
        if event.end_date_time <= datetime.now() and not reservation.rating_sent:
            user = reservation.user

            rating_url = f"{base_frontend_url}/event/{event.id}/create/rating"

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
            print(f"Generando enlace para {user.email}: {rating_url}")

    db.commit()

def send_event_cancellation_email(user_email, user_name, event_title):
    subject = f"Cancelación del evento {event_title}"

    html = render_email_template(
        "emails/event_cancellation.html",
        {
            "user_name": user_name,
            "event_title": event_title
        }
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = user_email
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def send_new_event_email(to_email, organizer_name, event_title, event_url):
    subject = f"Nuevo evento de {organizer_name}: {event_title}"

    html = render_email_template(
        "emails/new_event_notification.html",
        {
            "organizer_name": organizer_name,
            "event_title": event_title,
            "event_url": event_url
        }
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
