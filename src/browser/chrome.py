import chromedriver_binary
from selenium import webdriver

from browser import browser


class Chrome(browser.Browser):
    def __init__(self, absolute_user_data_dir=None):
        super().__init__()

        _ = chromedriver_binary  # Sorry, to avoid imports optimization.

        options = webdriver.ChromeOptions()
        if absolute_user_data_dir is not None:
            options.add_argument(f"--user-data-dir={absolute_user_data_dir}")

        self._driver = webdriver.Chrome(options=options)
