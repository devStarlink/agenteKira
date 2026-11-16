import mss
import io

from PIL import Image
from src.privated_engine import secure_screen

def take_screenshot() -> tuple[list[bytes], str] | str:
    secure, info = secure_screen()

    if not secure:
        print(f"[PRIVACIDAD] {info}")
        return "BLOQUEADO"

    with mss.mss() as sct:
        capturas = []
        for monitor in sct.monitors[1:]:
            capture = sct.grab(monitor)
            img = Image.frombytes("RGB", capture.size, capture.bgra, "raw", "BGRX")
            img.thumbnail((960, 540))

            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=75)
            capturas.append(buffer.getvalue())
        
        return capturas, info

    