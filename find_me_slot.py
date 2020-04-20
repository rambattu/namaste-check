from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import re
import smtplib
import time
import yaml

SETTINGS_FILE = "settings.yaml"

cfg = {}
with open(SETTINGS_FILE,"r") as yamlf:
    cfg = yaml.load(yamlf, Loader=yaml.SafeLoader)

OPEN_BROWSER = cfg['OPEN_BROWSER']
CHROMEDRIVER = "./chromedriver"

MAIN_SITE = "https://namastecart.com/login"
CHECKOUT_URL = "https://namastecart.com/cart/checkout"

SITE_LOGIN_BUTTON = '//button[@type="submit"]'
EMAIL_FIELD_ID = "email"
PASSWD_FIELD_ATTR = '//input[@name="password"]'

LOCATION = cfg['LOCATION']

NAMASTE_EMAIL = cfg['NAMASTE_EMAIL'] # 
NAMASTE_PASSWD = cfg['NAMASTE_PASSWD'] #
SENDER_GMAIL_ID = cfg['SENDER_GMAIL_ID']
SENDER_GMAIL_PWD = cfg['SENDER_GMAIL_PWD']
RECEIVER_GMAIL_ID = cfg['RECEIVER_GMAIL_ID']

GMAIL_SMTP = 'smtp.gmail.com'
GMAIL_SMTP_PORT = 587

WAIT_FOR_MAIN_SITE = 5
WAIT_FOR_LOCATION = 5
WAIT_FOR_INPUT = 2
WAIT_FOR_LOGGING_IN = 10

ROUND_WAIT_TIME = 30 # 3 minutes
# ROUND_WAIT_TIME = 3*60 # 3 minutes
ROUND_COUNT = 160 # Roughly 8 hours

class BrowseForMe:

    def __init__(self):
        opts = Options()
        if OPEN_BROWSER == 0:
            opts.headless = True
        self.browser = webdriver.Chrome(CHROMEDRIVER, options=opts)


    def login(self):
        self.browser.get(MAIN_SITE)
        time.sleep(WAIT_FOR_MAIN_SITE)

        email_field =self.browser.find_element_by_id(EMAIL_FIELD_ID)
        if not email_field:
            print("FAILED TO LOCATE EMAIL FIELD ON LOGIN PAGE")
            self.close_and_quit()
        email_field.send_keys(NAMASTE_EMAIL)
        time.sleep(WAIT_FOR_INPUT)

        passwd_field =self.browser.find_element_by_xpath(PASSWD_FIELD_ATTR)
        if not passwd_field:
            print("FAILED TO LOCATE PASSWORD FIELD ON LOGIN PAGE")
            self.close_and_quit()
        passwd_field.send_keys(NAMASTE_PASSWD)
        time.sleep(WAIT_FOR_INPUT)

        login_btn =self.browser.find_element_by_xpath(SITE_LOGIN_BUTTON)
        if not login_btn:
            print("FAILED TO LOCATE LOGIN BUTTON ON MAIN PAGE")
            self.close_and_quit()
        login_btn.click()
        time.sleep(WAIT_FOR_LOGGING_IN)

    def select_location(self):
        loc_btn = self.browser.find_element_by_xpath('//*[@id="location-list"]/li[' + str(LOCATION) + ']/h4/a')
        if not loc_btn:
            print("FAILED TO FIND LOCATION BUTTON")
            self.close_and_quit()
        loc_btn.click()
        time.sleep(WAIT_FOR_LOGGING_IN)
        loc_after_prompt = self.browser.find_element_by_xpath('//*[@id="price-list-' + str(LOCATION-1) + '"]/ul/li/p')
        if not loc_after_prompt:
            print("FAILED TO FIND LOCATION PROMPT")
            self.close_and_quit()
        loc_after_prompt.click()
        time.sleep(WAIT_FOR_LOCATION)

    def get_to_checkout(self):
        self.browser.get(CHECKOUT_URL)
        time.sleep(WAIT_FOR_LOCATION)

    def check_for_avail(self):
        unavail_text_container = None
        try:
            unavail_text_container = \
                self.browser.find_element_by_xpath('/html/body/div[2]/section/div/div/div[2]/div/div/div/h4')
        except NoSuchElementException as exception:
            print("Probably available, we don't see the unavailability banner")
            self.email("NAMASTECART AVAILABLE\n" + self.get_times_msg())
            self.close_and_quit()
        
        unavail_text = unavail_text_container.text
        match = re.search("All delivery windows are full at the moment", unavail_text)
        if match:
            # Delivery isn't still available, retry
            # time.sleep(3*60)
            self.get_to_checkout()
            return
        else:
            self.email(unavail_text)
            self.close_and_quit()
        return

    def get_times_msg(self):
        msg = ""
        exc = False
        try:
            day = self.browser.find_element_by_xpath('//*[@id="checkoutForm"]/div[1]/div[2]/select/option')
        except NoSuchElementException as exception:
            print("CANNOT GET DELIVERY DAY")
            exc = True
        if not exc:
            msg += day.text + "\n"

        exc = False
        try:
            slot = self.browser.find_element_by_xpath('//*[@id="checkoutForm"]/div[1]/div[3]/select/option')
        except NoSuchElementException as exception:
            print("CANNOT GET DELIVERY TIME")
            exc = True
        if not exc:
            msg += slot.text + "\n"

        return msg


    def send_email(self, message):
        if cfg['SENDER_GMAIL_ID'] and cfg['SENDER_GMAIL_PWD'] and \
            cfg['RECEIVER_GMAIL_ID']:
            self.email(message)


    def close_and_quit(self):
        self.browser.close()
        quit()


    def loop_till_you_shop(self):

        for round in range(ROUND_COUNT):
            self.check_for_avail()
            print("Round :", round+1)
            time.sleep(ROUND_WAIT_TIME)


    def email(self, message):
        # establishing connection to the gmail server with domain name and port. 
        # This differs with each email provider
        connection = smtplib.SMTP(GMAIL_SMTP,GMAIL_SMTP_PORT)
        
        # say hello to the server
        connection.ehlo()
        
        # starting encrypted TLS connection
        connection.starttls()
        
        # log into gmail server with your main address and password
        connection.login(SENDER_GMAIL_ID, SENDER_GMAIL_PWD)
        
        # sending mail to yourself informing you about the price of camera
        connection.sendmail(SENDER_GMAIL_ID, RECEIVER_GMAIL_ID, message)
        
        # ending connection
        connection.quit()

if __name__ == '__main__':
    browse = BrowseForMe()
    browse.login()
    browse.select_location()
    browse.get_to_checkout()
    browse.loop_till_you_shop()
    browse.close_and_quit()

