import time

from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from utils.web_driver_utils import WebDriverUtils

fake = Faker()
def go_to_contact_page(driver):
    return WebDriverUtils(driver=driver)\
        .click_by_css_selector(css_selector='a[data-test="nav-contact"]')
def generateMsg():
    text = fake.paragraph();
    text_length = len(text)
    while text_length < 50 or text_length > 250:
        text = fake.paragraph()
        text_length = len(text)
    return text

def fill_contact_form(driver=None,
                            web_driver_utils=None,
                            first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            email=fake.email(),
                            message=None,
                            ):

    web_driver_utils = web_driver_utils or WebDriverUtils(driver=driver)
    web_driver_utils\
        .fill(xpath='//*[@id="first_name"]', value=first_name)\
        .fill(xpath='//*[@id="last_name"]', value=last_name)\
        .fill(xpath='//*[@id="email"]', value=email) \
        .select_option(xpath='//*[@id="subject"]', index=1)\
        .fill(xpath='//*[@id="message"]', value=message)\
        .click_and_sleep(xpath='//*[@class="btnSubmit"]',seconds=1)

def message_is_send(driver=None):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".alert"))
    )
    return element.is_displayed() and element.text=="Thanks for your message! We will contact you shortly."

def error_is_displayed(driver=None):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "#message_alert"))
    )
    return element.is_displayed() and element.text=="Message must be minimal 50 characters"



