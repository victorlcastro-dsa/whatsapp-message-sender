import os
import logging
from typing import Tuple


class Config:
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"
    )
    CONTACTS_FILE_PATH: str = os.getenv(
        "CONTACTS_FILE_PATH", "../Lista de Contatos.ods"
    )
    BROWSER_DETACH: bool = os.getenv("BROWSER_DETACH", "True").lower() in (
        "true",
        "1",
        "t",
    )
    WAIT_TIMEOUT: int = int(os.getenv("WAIT_TIMEOUT", 120))
    MESSAGE_DELAY: Tuple[int, int] = tuple(
        map(int, os.getenv("MESSAGE_DELAY", "10,15").split(","))
    )

    @staticmethod
    def configure_logging():
        logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


config = Config()
