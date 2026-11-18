import time
import psutil

class SystemEventsManager:
    def __init__(self, cooldown: int = 3600):
        self.cooldown = cooldown
        self.last_event_time = 0
        self.watched_apps = {
            "code.exe": "Visual Studio Code",
            "steam.exe": "Steam",
            "spotify.exe": "Spotify",
        }
        self.known_processes = self._get_current_processes()

    def _get_current_processes(self) -> set:
        processes = set()
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"]:
                    processes.add(proc.info["name"].lower())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes


    def check_events(self) -> str | None:
        now = time.time()
        current_processes = self._get_current_processes()
        detected_app = None

        for exe_name, friendly_name in self.watched_apps.items():
            if exe_name in current_processes and exe_name not in self.known_processes:
                detected_app = friendly_name
                break

        self.known_processes = current_processes

        if detected_app and (now - self.last_event_time) >= self.cooldown:
            self.last_event_time = now
            return detected_app

        return None 