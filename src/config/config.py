import os


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Configurações de logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT = os.getenv(
            "LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"
        )

        # Configurações de arquivo de contatos
        self.CONTACTS_FILE_PATH = os.getenv(
            "CONTACTS_FILE_PATH", "../Lista de Contatos.ods"
        )

        # Configurações do navegador
        self.BROWSER_DETACH = os.getenv("BROWSER_DETACH", "True").lower() in (
            "true",
            "1",
            "t",
        )
        self.WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", 120))
        self.MESSAGE_DELAY = tuple(
            map(int, os.getenv("MESSAGE_DELAY", "10,15").split(","))
        )


# Instância global da configuração
config = Config()
