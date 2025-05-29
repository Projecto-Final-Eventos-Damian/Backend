import os

def get_event_image_path(image_url: str) -> str:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    image_path = os.path.join(project_root, image_url.lstrip("/"))
    return image_path
