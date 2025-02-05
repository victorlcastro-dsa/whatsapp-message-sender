import logging
import argparse
from services import BrowserManager, ContactLoader, WhatsAppMessageSender
from config import config

# Logging configuration
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


def main(file=config.CONTACTS_FILE_PATH, detach=config.BROWSER_DETACH, wait_timeout=config.WAIT_TIMEOUT, message_delay=config.MESSAGE_DELAY):
    """Main function of the script."""
    try:
        contact_loader = ContactLoader(file)
        contacts = contact_loader.load_contacts()
        if contacts is None:
            return

        with BrowserManager(detach=detach) as browser:
            sender = WhatsAppMessageSender(
                browser, contacts, wait_timeout=wait_timeout, message_delay=message_delay)
            sender.send_messages()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp Message Sender")
    parser.add_argument(
        "--file", type=str, default=config.CONTACTS_FILE_PATH, help="Path to the contacts file")
    parser.add_argument("--detach", type=bool, default=config.BROWSER_DETACH,
                        help="Whether to detach the browser")
    parser.add_argument("--wait-timeout", type=int,
                        default=config.WAIT_TIMEOUT, help="Timeout for waiting for elements")
    parser.add_argument("--message-delay", type=int, nargs=2,
                        default=config.MESSAGE_DELAY, help="Delay range for sending messages")

    args = parser.parse_args()
    main(args.file, args.detach, args.wait_timeout, tuple(args.message_delay))
