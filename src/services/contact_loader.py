import pandas as pd
import os
import logging


class ContactLoader:
    def __init__(self, file):
        self.file = file

    def load_contacts(self):
        """Loads contacts from the ODS file."""
        if not os.path.exists(self.file):
            logging.error(f"Error: The file '{
                          self.file}' was not found in the folder.")
            return None
        try:
            return pd.read_excel(self.file, engine="odf")
        except Exception as e:
            logging.error(f"Error loading contacts: {e}")
            return None
