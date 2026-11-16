import pygetwindow as gw

FORBIDDEN_WORDS = (
    "banco",
    "bank",
    "paypal",
    "password",
    "contraseña",
    "bitwarden",
    "1password",
    ".env",
    "incógnito",
    "inprivate",
    "whatsapp",
    "telegram",
    "gmail",
    "outlook",
)

def secure_screen() -> tuple[bool, str]:
    try:
        for window in gw.getAllWindows():
            title = window.title.lower().strip()

            if not title:
                continue

            for forbidden in FORBIDDEN_WORDS:
                if forbidden in title:
                    return False, f"Ventana sensible detectada: '{window.title}'"

        active = gw.getActiveWindow()
        title_active = active.title if active and active.title else "Escritorio"
        return True, title_active

    except Exception as e:
         return False, f"Error verificando ventanas: {e}"