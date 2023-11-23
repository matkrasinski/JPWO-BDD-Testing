from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

class Identity:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.email == other.email and self.password == other.password


admin = Identity("admin@practicesoftwaretesting.com", "welcome01")
customer = Identity("customer@practicesoftwaretesting.com", "welcome01")

class WebDriverUtils:
    def __init__(self, driver:WebDriver) -> None:
        self.driver = driver

    def login(self, identity: Identity):
        self.driver.get("https://practicesoftwaretesting.com/#/auth/login")

        wait = WebDriverWait(self.driver, 10)
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


    def login_as_admin(self):
        self.login(admin)
        return self


    def login_as_customer(self):
        self.login(customer)
        return self


    def click(self, xpath):
        element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        return self

    def click_and_sleep(self, xpath, seconds):
        element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        sleep(seconds)
        return self


    def click_by_css_selector(self, css_selector):
        element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        element.click()
        return self


    def fill(self, xpath, value):
        element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        element.clear()
        element.send_keys(value)
        return self

    def fill_and_press_return(self, xpath, value):
        element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        element.clear()
        element.send_keys(value)
        element.send_keys(Keys.RETURN)
        return self


    def select_option(self, xpath, index):
        element = Select(WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath))))
        element.select_by_index(index)
        return self


    def is_value_in_element_text(self, table_xpath, value):
        element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, table_xpath)))
        return value in element.text


    def get_element_text(self, xpath) -> str:
        element = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        return element.text
