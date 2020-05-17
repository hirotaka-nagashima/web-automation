import datetime as dt

from browser import chrome
from tools import comicseeker
from tools import jankara
from tools.twitter import csvhandler
from tools.twitter import developer
from tools.twitter import unlocker
from utils import sms


def main():
    chrome_user_data_dir = r"C:\~"
    browser = chrome.Chrome(absolute_user_data_dir=chrome_user_data_dir)
    sms_ = sms.SMS(browser)
    sms_.connect()


if __name__ == "__main__":
    main()
