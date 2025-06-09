import os
import base64

def get_event_image_path(image_url: str) -> str:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if not image_url:
        image_url = "public/images/events/default_event.png"
    image_path = os.path.join(project_root, image_url.lstrip("/"))
    return image_path

def encode_image_to_base64(path):
    if not os.path.exists(path):
        print(f"[ERROR] Imagen no encontrada: {path}")
        return ""
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")