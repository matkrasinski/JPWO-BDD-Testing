from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class Auth:
    customer_email = "customer@practicesoftwaretesting.com"
    customer_password = "welcome01"

    @staticmethod
    def login(driver: WebDriver, email: str = customer_email, password: str = customer_password):
        driver.get("https://practicesoftwaretesting.com/#/auth/login")

        wait = WebDriverWait(driver, 10)
        signin_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-test="nav-sign-in"]')))
        signin_button.click()

        email_field = wait.until(ec.element_to_be_clickable((By.ID, "email")))
        email_field.clear()
        email_field.send_keys(email)

        password_field = wait.until(ec.element_to_be_clickable((By.ID, "password")))
        password_field.clear()
        password_field.send_keys(password)

        signin_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.btnSubmit')))
        signin_button.click()
