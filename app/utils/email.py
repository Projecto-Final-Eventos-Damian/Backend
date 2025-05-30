import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from app import models, schemas, crud
from app.database import get_db
import os

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

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