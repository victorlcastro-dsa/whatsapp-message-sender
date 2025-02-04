import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import urllib.parse
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WhatsAppMessageSender:
    def __init__(self, file):
        self.file = file
        self.browser = self.setup_browser()

    def setup_browser(self):
        """Configures and returns the browser with automatic ChromeDriver."""
        chrome_service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(service=chrome_service, options=options)
        return browser

    def wait_for_element(self, element_id, timeout=30):
        """Waits until a specific element is loaded in the browser."""
        for _ in range(timeout):
            if len(self.browser.find_elements(By.ID, element_id)) > 0:
                return True
            time.sleep(1)
        return False

    def load_contacts(self):
        """Loads contacts from the ODS file."""
        if not os.path.exists(self.file):
            logging.error(f"Error: The file '{self.file}' was not found in the folder.")
            return None
        return pd.read_excel(self.file, engine="odf")

    def send_message(self, number, message):
        """Sends a message to a specific contact."""
        self.browser.get(f'https://web.whatsapp.com/send?phone={number}&text={message}')
        if self.wait_for_element('main'):
            input_box = self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p')
            input_box.send_keys(Keys.ENTER)
            time.sleep(random.randint(10, 15))
        else:
            logging.error(f"Error loading the conversation with the number {number}.")

    def send_messages(self):
        """Sends messages to all loaded contacts."""
        self.browser.get('https://web.whatsapp.com/')
        logging.info("Scan the WhatsApp Web QR Code to continue...")

        if not self.wait_for_element('side'):
            logging.error("Error loading WhatsApp Web.")
            return

        contacts = self.load_contacts()
        if contacts is None:
            return

        base_message = contacts['Mensagem Base'].dropna().iloc[0]

        for i, row in contacts.iterrows():
            number = str(row['Contatos']).strip()
            link = row['Link']
            final_message = f"{base_message} {link}"
            encoded_final_message = urllib.parse.quote(final_message)
            self.send_message(number, encoded_final_message)

        logging.info("Messages sent successfully!")
        self.browser.quit()

def main():
    """Main function of the script."""
    try:
        file = "Teste.ods"
        sender = WhatsAppMessageSender(file)
        sender.send_messages()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
