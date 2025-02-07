import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from config import config


class BrowserManager:
    _instance: "BrowserManager" = None
    browser: webdriver.Chrome

    def __new__(cls, *args, **kwargs) -> "BrowserManager":
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, detach: bool = config.BROWSER_DETACH) -> None:
        if not hasattr(self, "browser"):
            self.browser = self.setup_browser(detach)

    def setup_browser(self, detach: bool) -> webdriver.Chrome:
        """Configures and returns the browser with automatic ChromeDriver."""
        try:
            chrome_service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", detach)
            browser = webdriver.Chrome(service=chrome_service, options=options)
            logging.info("Browser successfully configured and launched.")
            return browser
        except WebDriverException as e:
            logging.error(f"WebDriver error setting up browser: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error setting up browser: {e}")
            raise

    def __enter__(self) -> webdriver.Chrome:
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            self.browser.quit()
            logging.info("Browser successfully closed.")
        except WebDriverException as e:
            logging.error(f"WebDriver error closing browser: {e}")
        except Exception as e:
            logging.error(f"Unexpected error closing browser: {e}")
