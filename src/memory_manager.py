from collections import deque

recent_history = deque(maxlen=4)

def save_messages(rol: str, contenido: str) -> None:
    content_clear = contenido[:300] + "..." if len(contenido) > 300 else contenido
    recent_history.append({
        'role': rol,
        'content': content_clear,
    })

def get_history() -> list[dict]:
    return list(recent_history)

def clear_memory() -> None:
    recent_history.clear()

