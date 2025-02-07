import pandas as pd
import logging
from pathlib import Path
from config import config
from typing import Optional


class ContactLoader:
    def __init__(self, file: str = config.CONTACTS_FILE_PATH) -> None:
        self._file: str = file

    def load_contacts(
        self,
    ) -> Optional[pd.DataFrame]:
        """Loads contacts from the ODS file."""
        file_path = Path(self._file)
        if not file_path.exists():
            logging.error(
                f"Error: The file '{self._file}' was not found in the folder."
            )
            return None
        try:
            return pd.read_excel(self._file, engine="odf")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            return None
        except pd.errors.ExcelFileError as e:
            logging.error(f"Error loading contacts: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None
