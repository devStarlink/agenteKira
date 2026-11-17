import mss
import io

from PIL import Image
from src.privated_engine import secure_screen

def take_screenshot() -> tuple[bytes, str] | str:
    secure, info = secure_screen()

    if not secure:
        print(f"[PRIVACIDAD] {info}")
        return "BLOQUEADO"

    with mss.mss() as sct:
        monitor = sct.monitors[2]
        capture = sct.grab(monitor)
        img = Image.frombytes("RGB", capture.size, capture.bgra, "raw", "BGRX")
        img.thumbnail((1280, 720))

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
        return buffer.getvalue(), info

    