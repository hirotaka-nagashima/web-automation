import os

from browser import chrome
from utils import sms


def main():
    chrome_user_data_dir = os.path.abspath(__file__ + "/../../data/chrome")
    browser = chrome.Chrome(absolute_user_data_dir=chrome_user_data_dir)
    sms_ = sms.SMS(browser)
    sms_.connect()


if __name__ == "__main__":
    main()
