import os


class Config:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")
    CONTACTS_FILE_PATH = os.getenv("CONTACTS_FILE_PATH", "../Lista de Contatos.ods")
    BROWSER_DETACH = os.getenv("BROWSER_DETACH", "True").lower() in ("true", "1", "t")
    WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", 120))
    MESSAGE_DELAY = tuple(map(int, os.getenv("MESSAGE_DELAY", "10,15").split(",")))


config = Config()
