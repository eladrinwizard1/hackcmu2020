# Twitter Bot Source:
# https://towardsdatascience.com/how-i-built-a-twitter-bot-using-python-and-selenium-c036bfff6af8

import markovify
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.common.action_chains import ActionChains


class TwitterBot:
    def __init__(self, username, password):
        self.browser = webdriver.Chrome("chromedriver_win32/chromedriver.exe")
        self.username = username
        self.password = password
        self.sign_in()

    def sign_in(self):
        self.browser.get("https://www.twitter.com/login")
        time.sleep(5)

        username_input = self.browser.find_element_by_name(
            "session[username_or_email]")
        password_input = self.browser.find_element_by_name("session[password]")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def tweet(self, text):
        if len(text) < 280:
            tweet = self.browser.find_element_by_xpath("""//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div
                                                      /div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div
                                                      /div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div
                                                      /div/div/div""")
            tweet.send_keys(text)
            ActionChains(self.browser) \
                .key_down(Keys.CONTROL) \
                .send_keys(Keys.COMMAND, Keys.ENTER) \
                .key_up(Keys.CONTROL) \
                .perform()
        else:
            print("Tweet too long")


if __name__ == "__main__":
    with open("credentials.json", "r") as f:
        credentials = json.load(f)
    un = credentials["username"]
    p = credentials["password"]
    t = TwitterBot(un, p)
    t.tweet("test")
