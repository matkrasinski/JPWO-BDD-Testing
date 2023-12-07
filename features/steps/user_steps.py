from datetime import datetime

from behave import *
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.registration_utils import login_page_is_displayed, \
    registration_error_is_displayed
from utils.web_driver_utils import WebDriverUtils

use_step_matcher("re")

driver: None | WebDriver = None
wait = None
base_url = "https://practicesoftwaretesting.com"

web_driver_utils: None | WebDriverUtils = None
fake = Faker()

latest_email: str | None = None


@given("I run Chrome Browser")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    global driver, wait, web_driver_utils
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)

    web_driver_utils = WebDriverUtils(driver=driver)


@given("I go to the registration page from home page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    web_driver_utils \
        .click_by_css_selector(css_selector='a[data-test="nav-sign-in"]') \
        .click(xpath="//div[@class='col-lg-6 auth-form']//form//div[@class='input-group mb-3'][4]//p//a[1]")


@when("I fill registration form with valid random data")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = '01.01.2000'
    address = fake.address()
    postcode = fake.postcode()
    city = fake.city()
    state = fake.state()
    phone_number = ''.join(char for char in fake.phone_number() if char.isdigit())
    email = fake.email()
    password = fake.password()

    web_driver_utils \
        .fill(xpath='//*[@id="first_name"]', value=first_name) \
        .fill(xpath='//*[@id="last_name"]', value=last_name) \
        .fill(xpath='//*[@id="dob"]', value=dob) \
        .fill(xpath='//*[@id="address"]', value=address) \
        .fill(xpath='//*[@id="postcode"]', value=postcode) \
        .fill(xpath='//*[@id="city"]', value=city) \
        .fill(xpath='//*[@id="state"]', value=state) \
        .select_option(xpath='//*[@id="country"]', index=42) \
        .fill(xpath='//*[@id="phone"]', value=phone_number) \
        .fill(xpath='//*[@id="email"]', value=email) \
        .fill(xpath='//*[@id="password"]', value=password)

    global latest_email
    latest_email = email


@step('I press "Register" button')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    web_driver_utils \
        .click_and_sleep(xpath='//div[@class="col-lg-8 auth-form"]//form//button[@class="btnSubmit mb-3"]', seconds=1)


@then("I am on the login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert login_page_is_displayed(driver), "User is not on the login page after submission."


@then("I fill registration form with latest email")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = '01.01.2000'
    address = fake.address()
    postcode = fake.postcode()
    city = fake.city()
    state = fake.state()
    phone_number = ''.join(char for char in fake.phone_number() if char.isdigit())
    password = fake.password()

    web_driver_utils \
        .fill(xpath='//*[@id="first_name"]', value=first_name) \
        .fill(xpath='//*[@id="last_name"]', value=last_name) \
        .fill(xpath='//*[@id="dob"]', value=dob) \
        .fill(xpath='//*[@id="address"]', value=address) \
        .fill(xpath='//*[@id="postcode"]', value=postcode) \
        .fill(xpath='//*[@id="city"]', value=city) \
        .fill(xpath='//*[@id="state"]', value=state) \
        .select_option(xpath='//*[@id="country"]', index=42) \
        .fill(xpath='//*[@id="phone"]', value=phone_number) \
        .fill(xpath='//*[@id="email"]', value=latest_email) \
        .fill(xpath='//*[@id="password"]', value=password)


@then("I see error message about existing email")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert registration_error_is_displayed(driver), "Somehow the user was able to register with used email"


@when("I go to registration page from login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    web_driver_utils \
        .click(xpath="//div[@class='col-lg-6 auth-form']//form//div[@class='input-group mb-3'][4]//p//a[1]")


@when("I fill registration form with random data containing invalid date of birth")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = datetime.now().strftime('%d.%m.%Y')
    address = fake.address()
    postcode = fake.postcode()
    city = fake.city()
    state = fake.state()
    phone_number = ''.join(char for char in fake.phone_number() if char.isdigit())
    email = fake.email()
    password = fake.password()

    web_driver_utils \
        .fill(xpath='//*[@id="first_name"]', value=first_name) \
        .fill(xpath='//*[@id="last_name"]', value=last_name) \
        .fill(xpath='//*[@id="dob"]', value=dob) \
        .fill(xpath='//*[@id="address"]', value=address) \
        .fill(xpath='//*[@id="postcode"]', value=postcode) \
        .fill(xpath='//*[@id="city"]', value=city) \
        .fill(xpath='//*[@id="state"]', value=state) \
        .select_option(xpath='//*[@id="country"]', index=42) \
        .fill(xpath='//*[@id="phone"]', value=phone_number) \
        .fill(xpath='//*[@id="email"]', value=email) \
        .fill(xpath='//*[@id="password"]', value=password)


@then("I see error message about invalid date of birth")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert registration_error_is_displayed(driver), "User is too young to register an account."
