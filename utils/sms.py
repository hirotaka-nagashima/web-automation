from browser import browser


class SMS:
    """Handles SMS."""

    _URL = "https://messages.google.com/web/conversations"
    _URL_TO_AUTH = "https://messages.google.com/web/authentication"

    def __init__(self, browser_):
        self._tab_id = None  # to switch tabs
        self._browser = browser_  # type: browser.Browser

    def connect(self):
        """Opens Messages for web in a current tab."""
        # Check whether the page is opened already.
        url_pattern = f"{SMS._URL}|{SMS._URL_TO_AUTH}"
        tab_id = self._browser.find_tab(url_pattern)
        if tab_id is None:
            self._browser.open(SMS._URL)
        else:
            self._browser.switch_to(tab_id)

        # Authenticate a user if needed.
        qr_code = "mw-qr-code"  # Authentication is required.
        conversations = "mws-conversations-list"  # Already authenticated.
        self._browser.wait_any_display(qr_code, conversations)
        if self._browser.exists(qr_code):
            # Wait for authentication.
            print("Authentication is required.")
            self._browser.wait_display(conversations)
            print("Thanks!")

            # Save a cookie for next use.
            saves_cookie = "button[data-e2e-remember-this-computer-confirm]"
            self._browser.click(saves_cookie, waits=True)

        self._tab_id = self._browser.tab_id

    def receive(self):
        """Waits for a SMS then returns it."""
        initial_tab_id = self._browser.tab_id
        self._browser.switch_to(self._tab_id)

        # Wait for a message.
        while True:
            unread = ".text-content.unread"
            dialog = "mws-dialog"
            self._browser.wait_any_display(unread, dialog)
            if self._browser.exists(dialog):
                # Hide the dialog that appears when Messages for web is opened
                # in multiple tabs.
                self._browser.click(f"{dialog} button")
            if self._browser.exists(unread):
                break

        self._browser.click(unread)
        last_msg = "mws-message-wrapper[is-last='true'] .text-msg"
        msg = self._browser.get_text(last_msg, waits=True)

        # Go back to the initial tab.
        self._browser.switch_to(initial_tab_id)
        return msg
