import time

class InactivityManager:
    def __init__(self, downtime: int = 60, cooldown: int = 120):
        self.downtime = downtime
        self.cooldown = cooldown
        self.last_interaction = time.time()
        self.last_warning = 0

    def log_interaction(self):
        self.last_interaction = time.time()

    def must_speak(self) -> bool:
        now = time.time()

        if (now - self.last_warning) < self.cooldown:
            return False

        if (now - self.last_warning) >= self.cooldown:
            self.last_warning = now
            return True

        return False