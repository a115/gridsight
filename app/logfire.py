import logfire
from app.configuration.app import app_settings


class Logfire:
    def __init__(self, service_name=None):
        self.token = app_settings.logfire_token
        self.service_name = service_name or app_settings.app_name
        logfire.configure(token=self.token, service_name=self.service_name)

    def log_message(self, message: str) -> None:
        """Log a message to Logfire."""
        logfire.info(message)
        return None
