from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrowserManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, detach=True):
        if not hasattr(self, 'browser'):
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
