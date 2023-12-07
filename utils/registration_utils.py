from utils.web_driver_utils import WebDriverUtils
from faker import Faker
from datetime import datetime, timedelta
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from time import sleep


fake = Faker()

def go_to_login_page(driver):
    return WebDriverUtils(driver=driver)\
        .click_by_css_selector(css_selector='a[data-test="nav-sign-in"]')


def register_from_login_page(driver=None,
                            web_driver_utils=None,
                            first_name=fake.first_name(),
                            last_name=fake.last_name(),
                            dob=None,
                            address=fake.address(),
                            postcode=fake.postcode(),
                            city=fake.city(),
                            state=fake.state(),
                            phone_number=''.join(char for char in fake.phone_number() if char.isdigit()),
                            email=fake.email(),
                            password=fake.password(),
                            seconds=1
                            ):
    dob = dob or generate_random_date_of_birth()
    web_driver_utils = web_driver_utils or WebDriverUtils(driver=driver)

    web_driver_utils\
        .click(xpath="//div[@class='col-lg-6 auth-form']//form//div[@class='input-group mb-3'][4]//p//a[1]")\
        .fill(xpath='//*[@id="first_name"]', value=first_name)\
        .fill(xpath='//*[@id="last_name"]', value=last_name)\
        .fill(xpath='//*[@id="dob"]', value=dob)\
        .fill(xpath='//*[@id="address"]', value=address)\
        .fill(xpath='//*[@id="postcode"]', value=postcode)\
        .fill(xpath='//*[@id="city"]',value=city)\
        .fill(xpath='//*[@id="state"]', value=state)\
        .select_option(xpath='//*[@id="country"]', index=42)\
        .fill(xpath='//*[@id="phone"]', value=phone_number)\
        .fill(xpath='//*[@id="email"]', value=email)\
        .fill(xpath='//*[@id="password"]', value=password)\
        .click_and_sleep(xpath='//div[@class="col-lg-8 auth-form"]//form//button[@class="btnSubmit mb-3"]', seconds=seconds)


def login_page_is_displayed(driver=None):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//div[@class='col-lg-6 auth-form']//h3"))
    )
    return element.is_displayed() and element.text == "Login"


def registration_error_is_displayed(driver=None):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "app-register form.ng-dirty.ng-touched.ng-valid.ng-submitted .alert.alert-danger .help-block"))
    )
    return element.is_displayed()