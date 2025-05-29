from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from io import BytesIO
import os
from app.utils.files import get_event_image_path

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def generate_reservation_pdf(context: dict) -> bytes:
    if "event" in context and "image_url" in context["event"]:
        image_path = get_event_image_path(context["event"]["image_url"])
        if os.path.exists(image_path):
            context["event"]["image_path"] = f"file://{image_path}"
        else:
            print(f"No se encontró la imagen del evento: {image_path}")
            context["event"]["image_path"] = ""

    template = jinja_env.get_template("pdf/reservation_ticket.html")
    html_content = template.render(context)

    pdf_io = BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    return pdf_io.read()