import time
import random
import urllib.parse
import logging
from typing import List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import DataFrame
from config import config


class WhatsAppMessageSender:
    def __init__(
        self,
        browser: WebDriver,
        contacts: DataFrame,
        wait_timeout: int = config.WAIT_TIMEOUT,
        message_delay: Tuple[int, int] = config.MESSAGE_DELAY,
    ) -> None:
        self.browser = browser
        self.contacts = contacts
        self.wait_timeout = wait_timeout
        self.message_delay = message_delay

    def _wait_for_element(self, by: By, value: str) -> bool:
        """Waits until a specific element is loaded in the browser."""
        try:
            WebDriverWait(self.browser, self.wait_timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception as e:
            logging.error(f"Error waiting for element {value}: {e}")
            return False

    def _send_message(self, number: str, message: str) -> None:
        """Sends a message to a specific contact."""
        url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
        logging.info(f"Sending message to {number} with URL: {url}")
        self.browser.get(url)
        if self._wait_for_element(By.ID, "main"):
            try:
                input_box = self.browser.find_element(
                    By.XPATH,
                    '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p',
                )
                input_box.send_keys(Keys.ENTER)
                time.sleep(random.randint(*self.message_delay))
            except Exception as e:
                logging.error(f"Error sending message to {number}: {e}")
        else:
            logging.error(f"Error loading the conversation with the number {number}.")

    @staticmethod
    def _format_message(base_message: str, link: str) -> str:
        """Formats the final message to be sent."""
        if link:
            final_message = f"{base_message} {link}"
        else:
            final_message = base_message
        return urllib.parse.quote(final_message)

    def send_messages(self) -> None:
        """Sends messages to all loaded contacts."""
        self.browser.get("https://web.whatsapp.com/")
        logging.info("Scan the WhatsApp Web QR Code to continue...")

        if not self._wait_for_element(By.ID, "side"):
            logging.error("Error loading WhatsApp Web.")
            return

        base_messages: List[str] = self.contacts["Mensagem Base"].dropna().tolist()

        for i, row in self.contacts.iterrows():
            number: str = str(row["Contatos"]).strip()
            if not number or number.lower() == "nan":
                logging.warning(f"Skipping empty or invalid contact at row {i}.")
                continue
            if "." in number:
                number = number.split(".")[0]
            if not number.isdigit():
                logging.warning(f"Skipping invalid contact at row {i}: {number}")
                continue
            link: str = row.get("Link", "")
            base_message: str = random.choice(base_messages)
            encoded_final_message: str = self._format_message(base_message, link)
            try:
                self._send_message(number, encoded_final_message)
            except Exception as e:
                logging.error(f"Failed to send message to {number}: {e}")

        logging.info("Messages sent successfully!")
