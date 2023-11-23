import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.registration_utils import generate_random_date_of_birth, go_to_login_page, register_from_login_page, registration_error_is_displayed, login_page_is_displayed

from faker import Faker

class RegistrationTest(unittest.TestCase):
    
    fake = Faker()

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
            )
        self.driver.maximize_window()
        self.base_url = "https://practicesoftwaretesting.com"
        self.driver.get(self.base_url)
        self.wait = WebDriverWait(self.driver, 10)


    def test_user_registration(self):
        web_driver_utils = go_to_login_page(driver=self.driver)
        register_from_login_page(driver=self.driver, web_driver_utils=web_driver_utils)
        assert login_page_is_displayed(driver=self.driver), "User is not on the login page after submission."


    def test_duplicate_email_registration(self):
        email = Faker().email()
        web_driver_utils = go_to_login_page(driver=self.driver)
        register_from_login_page(driver=self.driver, web_driver_utils=web_driver_utils, email=email)
        assert login_page_is_displayed(driver=self.driver), "User is not on the login page after submission."

        register_from_login_page(web_driver_utils=web_driver_utils, email=email)
        assert registration_error_is_displayed(driver=self.driver), "Somehow the user was able to register with used email"


    def test_not_valid_dob(self):
        web_driver_utils = go_to_login_page(driver=self.driver)
        register_from_login_page(driver=self.driver, web_driver_utils=web_driver_utils, dob=generate_random_date_of_birth(min_age=10, max_age=11))
        assert registration_error_is_displayed(driver=self.driver), "User is too young to register an account."


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
