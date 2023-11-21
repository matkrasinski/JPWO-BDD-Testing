from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class Identity:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.email == other.email and self.password == other.password


admin = Identity("admin@practicesoftwaretesting.com", "welcome01")
customer = Identity("customer@practicesoftwaretesting.com", "welcome01")


def login(driver: WebDriver, identity: Identity):
    driver.get("https://practicesoftwaretesting.com/#/auth/login")

    wait = WebDriverWait(driver, 10)
    signin_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-test="nav-sign-in"]')))
    signin_button.click()

    email_field = wait.until(ec.element_to_be_clickable((By.ID, "email")))
    email_field.clear()
    email_field.send_keys(identity.email)

    password_field = wait.until(ec.element_to_be_clickable((By.ID, "password")))
    password_field.clear()
    password_field.send_keys(identity.password)

    signin_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.btnSubmit')))
    signin_button.click()


def login_as_admin(driver: WebDriver):
    login(driver, admin)


def login_as_customer(driver: WebDriver):
    login(driver, customer)


def click(driver, xpath):
    element = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    element.click()


def fill(driver, xpath, value):
    element = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    element.clear()
    element.send_keys(value)


def select_option(driver, xpath, index):
    element = Select(WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath))))
    element.select_by_index(index)


def is_value_in_element_text(driver, table_xpath, value):
    element = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, table_xpath)))
    return value in element.text
