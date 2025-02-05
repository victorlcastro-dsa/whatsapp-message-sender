import time
import random
import urllib.parse
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WhatsAppMessageSender:
    def __init__(self, browser, contacts, wait_timeout=120, message_delay=(10, 15)):
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
        url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
        logging.info(f"Sending message to {number} with URL: {url}")
        self.browser.get(url)
        if self.wait_for_element('main'):
            try:
                input_box = self.browser.find_element(
                    By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p')
                input_box.send_keys(Keys.ENTER)
                time.sleep(random.randint(*self.message_delay))
            except Exception as e:
                logging.error(f"Error sending message to {number}: {e}")
        else:
            logging.error(
                f"Error loading the conversation with the number {number}.")

    def send_messages(self):
        """Sends messages to all loaded contacts."""
        self.browser.get('https://web.whatsapp.com/')
        logging.info("Scan the WhatsApp Web QR Code to continue...")

        if not self.wait_for_element('side'):
            logging.error("Error loading WhatsApp Web.")
            return

        base_messages = self.contacts['Mensagem Base'].dropna().tolist()

        for i, row in self.contacts.iterrows():
            number = str(row['Contatos']).strip()
            if not number or number.lower() == 'nan':
                logging.warning(
                    f"Skipping empty or invalid contact at row {i}.")
                continue
            if '.' in number:
                number = number.split('.')[0]  # Remove decimal part if present
            link = row['Link']
            base_message = random.choice(base_messages)
            final_message = f"{base_message} {link}"
            encoded_final_message = urllib.parse.quote(final_message)
            self.send_message(number, encoded_final_message)

        logging.info("Messages sent successfully!")
