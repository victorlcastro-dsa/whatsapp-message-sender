import logging
import argparse
from services import BrowserManager, ContactLoader, WhatsAppMessageSender

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main(file, detach, wait_timeout, message_delay):
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
        "--file", type=str, default="../Lista de Contatos.ods", help="Path to the contacts file")
    parser.add_argument("--detach", type=bool, default=True,
                        help="Whether to detach the browser")
    parser.add_argument("--wait-timeout", type=int, default=120,
                        help="Timeout for waiting for elements")
    parser.add_argument("--message-delay", type=int, nargs=2,
                        default=[10, 15], help="Delay range for sending messages")

    args = parser.parse_args()
    main(args.file, args.detach, args.wait_timeout, tuple(args.message_delay))
