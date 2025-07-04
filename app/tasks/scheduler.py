from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.utils.email import send_rating_emails
from dotenv import load_dotenv
import os

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

def job_send_rating_emails():
    db: Session = SessionLocal()
    try:
        print("Ejecutando tarea de envío de ratings...")
        send_rating_emails(db, FRONTEND_URL)
    except Exception as e:
        logging.error(f"Error en tarea programada: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(job_send_rating_emails, "interval", hours=24)
    scheduler.add_job(job_send_rating_emails, "interval", minutes=1)
    scheduler.start()
