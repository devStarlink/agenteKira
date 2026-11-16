from collections import deque

recent_history = deque(maxlen=8)

def save_messages(rol: str, contenido: str) -> None:
    recent_history.append({
        'role': rol,
        'content': contenido,
    })

def get_history() -> list[dict]:
    return list(recent_history)

def clear_memory() -> None:
    recent_history.clear()

