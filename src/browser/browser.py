import abc
import re
from typing import Optional

from selenium.webdriver.common import by
from selenium.webdriver.remote import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import ui

from browser import ec


class Browser(abc.ABC):
    """Wrapper of the Selenium WebDriver."""

    @abc.abstractmethod
    def __init__(self):
        self._driver = None  # type: Optional[webdriver.WebDriver]

    @property
    def url(self):
        return self._driver.current_url

    @property
    def title(self):
        return self._driver.title

    @property
    def tab_id(self):
        return self._driver.current_window_handle

    def open(self, url, session=None):
        self._open(url, session, in_new_tab=False)

    def open_in_new_tab(self, url, session=None):
        self._open(url, session, in_new_tab=True)

    def open_new_tab(self):
        self._get_in_new_tab("about:blank")

    def _open(self, url, session, *, in_new_tab):
        # We must get the page before adding cookies.
        if in_new_tab:
            self._get_in_new_tab(url)
        else:
            self._driver.get(url)

        # Add cookies and reload.
        if session is not None:
            for cookie in session.cookies:
                cookie_dict = {"name": cookie.name, "value": cookie.value}
                self._driver.add_cookie(cookie_dict)
            self._driver.get(url)

    def _get_in_new_tab(self, url):
        script = f"window.open('{url}','_blank');"
        before_ids = set(self._driver.window_handles)
        self._driver.execute_script(script)
        after_ids = set(self._driver.window_handles)

        # Switch to the new tab.
        new_id = list(after_ids - before_ids)[0]
        self.switch_to(new_id)

    def switch_to(self, tab_id):
        self._driver.switch_to.window(tab_id)

    def find_tab(self, url_pattern):
        """
        Returns:
            Tab ID matched first or None.
        """
        initial_tab_id = self.tab_id

        # Find the tab by URL.
        target_tab_id = None
        for tab_id in self._driver.window_handles:
            self.switch_to(tab_id)
            if re.match(url_pattern, self.url) is not None:
                target_tab_id = tab_id
                break

        # Go back to the initial tab.
        self.switch_to(initial_tab_id)
        return target_tab_id

    def _get(self, selector, waits=False):
        elements = self._driver.find_elements_by_css_selector(selector)
        if not elements and waits:
            self.wait_display(selector)
        return elements[0] if elements else None

    def exists(self, selector):
        element = self._get(selector)
        return element is not None

    def get_text(self, selector, waits=False):
        element = self._get(selector, waits)
        return "" if element is None else element.text

    def get_attribute(self, selector, attribute_name, waits=False):
        element = self._get(selector, waits)
        return "" if element is None else element.get_attribute(attribute_name)

    def click(self, selector, waits=False):
        element = self._get(selector, waits)
        if element is not None:
            element.click()

    def input(self, selector, value, waits=False):
        element = self._get(selector, waits)
        if element is not None:
            element.send_keys(value)

    def submit(self, button_value, waits=False):
        self.click(f"input[type='submit'][value='{button_value}']", waits)

    def wait_display(self, selector, timeout=60):
        self.wait_any_display(selector, timeout=timeout)

    def wait_any_display(self, *selectors, timeout=60):
        locators = [(by.By.CSS_SELECTOR, s) for s in selectors]
        ecs = [expected_conditions.visibility_of_element_located(l_)
               for l_ in locators]
        any_ec = ec.AnyEC(*ecs)
        ui.WebDriverWait(self._driver, timeout).until(any_ec)
