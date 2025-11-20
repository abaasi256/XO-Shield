import os

class Settings:
    WIREGUARD_INTERFACE = os.getenv("WIREGUARD_INTERFACE", "wg0")
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))

settings = Settings()
