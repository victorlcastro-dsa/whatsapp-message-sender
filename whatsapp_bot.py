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
import argparse

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BrowserManager:
    def __init__(self, detach=True):
        self.browser = self.setup_browser(detach)

    def setup_browser(self, detach):
        """Configures and returns the browser with automatic ChromeDriver."""
        chrome_service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", detach)
        browser = webdriver.Chrome(service=chrome_service, options=options)
        return browser

    def __enter__(self):
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

class ContactLoader:
    def __init__(self, file):
        self.file = file

    def load_contacts(self):
        """Loads contacts from the ODS file."""
        if not os.path.exists(self.file):
            logging.error(f"Error: The file '{self.file}' was not found in the folder.")
            return None
        return pd.read_excel(self.file, engine="odf")

class WhatsAppMessageSender:
    def __init__(self, browser, contacts, wait_timeout=30, message_delay=(10, 15)):
        self.browser = browser
        self.contacts = contacts
        self.wait_timeout = wait_timeout
        self.message_delay = message_delay

    def wait_for_element(self, element_id):
        """Waits until a specific element is loaded in the browser."""
        for _ in range(self.wait_timeout):
            if len(self.browser.find_elements(By.ID, element_id)) > 0:
                return True
            time.sleep(1)
        return False

    def send_message(self, number, message):
        """Sends a message to a specific contact."""
        self.browser.get(f'https://web.whatsapp.com/send?phone={number}&text={message}')
        if self.wait_for_element('main'):
            input_box = self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p')
            input_box.send_keys(Keys.ENTER)
            time.sleep(random.randint(*self.message_delay))
        else:
            logging.error(f"Error loading the conversation with the number {number}.")

    def send_messages(self):
        """Sends messages to all loaded contacts."""
        self.browser.get('https://web.whatsapp.com/')
        logging.info("Scan the WhatsApp Web QR Code to continue...")

        if not self.wait_for_element('side'):
            logging.error("Error loading WhatsApp Web.")
            return

        base_message = self.contacts['Mensagem Base'].dropna().iloc[0]

        for i, row in self.contacts.iterrows():
            number = str(row['Contatos']).strip()
            link = row['Link']
            final_message = f"{base_message} {link}"
            encoded_final_message = urllib.parse.quote(final_message)
            self.send_message(number, encoded_final_message)

        logging.info("Messages sent successfully!")

def main(file, detach, wait_timeout, message_delay):
    """Main function of the script."""
    try:
        contact_loader = ContactLoader(file)
        contacts = contact_loader.load_contacts()
        if contacts is None:
            return

        with BrowserManager(detach=detach) as browser:
            sender = WhatsAppMessageSender(browser, contacts, wait_timeout=wait_timeout, message_delay=message_delay)
            sender.send_messages()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp Message Sender")
    parser.add_argument("--file", type=str, default="Teste.ods", help="Path to the contacts file")
    parser.add_argument("--detach", type=bool, default=True, help="Whether to detach the browser")
    parser.add_argument("--wait-timeout", type=int, default=30, help="Timeout for waiting for elements")
    parser.add_argument("--message-delay", type=int, nargs=2, default=[10, 15], help="Delay range for sending messages")

    args = parser.parse_args()
    main(args.file, args.detach, args.wait_timeout, tuple(args.message_delay))
