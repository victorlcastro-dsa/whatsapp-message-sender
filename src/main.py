import logging
import argparse
from typing import Tuple
from services import BrowserManager, ContactLoader, WhatsAppMessageSender
from config import config


def main(
    file: str = config.CONTACTS_FILE_PATH,
    detach: bool = config.BROWSER_DETACH,
    wait_timeout: int = config.WAIT_TIMEOUT,
    message_delay: Tuple[int, int] = config.MESSAGE_DELAY,
) -> None:
    """Main function of the script."""
    config.configure_logging()
    logging.info("Application started")

    try:
        contact_loader = ContactLoader(file)
        contacts = contact_loader.load_contacts()
        if contacts.empty:
            logging.error("No contacts loaded. Exiting.")
            return

        with BrowserManager(detach=detach) as browser:
            sender = WhatsAppMessageSender(
                browser,
                contacts,
                wait_timeout=wait_timeout,
                message_delay=message_delay,
            )
            sender.send_messages()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp Message Sender")
    parser.add_argument(
        "--file",
        type=str,
        default=config.CONTACTS_FILE_PATH,
        help="Path to the contacts file",
    )
    parser.add_argument(
        "--detach",
        type=bool,
        default=config.BROWSER_DETACH,
        help="Whether to detach the browser",
    )
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=config.WAIT_TIMEOUT,
        help="Timeout for waiting for elements",
    )
    parser.add_argument(
        "--message-delay",
        type=int,
        nargs=2,
        default=config.MESSAGE_DELAY,
        help="Delay range for sending messages",
    )

    args = parser.parse_args()
    main(args.file, args.detach, args.wait_timeout, tuple(args.message_delay))
