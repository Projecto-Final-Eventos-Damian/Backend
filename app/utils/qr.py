import qrcode
import base64
from io import BytesIO

def generate_qr_base64(code: str) -> str:
    qr = qrcode.make(code)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")