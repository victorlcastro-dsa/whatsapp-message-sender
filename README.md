# WhatsApp Message Sender

This project is a Python script to send messages via WhatsApp Web using Selenium. It loads a contact list from an ODS file and sends personalized messages to each contact.

## Project Structure

```
├── .gitignore
├── Lista de Contatos.ods
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── main.py
│   └── services/
│       ├── __init__.py
│       ├── browser_manager.py
│       ├── contact_loader.py
│       └── message_sender.py
```

## Requirements

- Python 3.8+
- Google Chrome
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/victorlcastro-dsa/whatsapp-message-sender.git
cd whatsapp-message-sender
```

2. Create a virtual environment and activate it:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

The project settings are in the `config.py` file. You can adjust the configuration parameters as needed, such as the contact file path, log level, wait time, and message delay.

## Usage

Prepare the `Lista de Contatos.ods` file with the contacts and base messages.
Run the main script:

```sh
python src/main.py
```

You can pass optional arguments to the script:

- `--file`: Path to the contact file (default: `../Lista de Contatos.ods`)
- `--detach`: Whether to detach the browser (default: `True`)
- `--wait-timeout`: Wait time for elements (default: `120`)
- `--message-delay`: Delay interval for sending messages (default: `(10, 15)`)

Example:

```sh
python src/main.py --file "my_contacts.ods" --detach False --wait-timeout 60 --message-delay 5 10
```

## File Structure

- `config.py`: Contains the project settings.
- `main.py`: Main script that coordinates contact loading, browser management, and message sending.
- `browser_manager.py`: Manages browser setup and control.
- `contact_loader.py`: Loads contacts from the ODS file.
- `message_sender.py`: Sends messages to the loaded contacts.
