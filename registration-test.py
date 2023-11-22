import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from utils import WebDriverUtils

import time 
from datetime import datetime, timedelta
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
        

    def generate_random_date_of_birth(self, min_age=18, max_age=100):
        random_age = Faker().random_int(min=min_age, max=max_age)
        
        birth_date = datetime.now() - timedelta(days=random_age * 365)
        
        formatted_birth_date = birth_date.strftime('%d.%m.%Y')
        
        return formatted_birth_date

    def login_page_is_displayed(self):
        element = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//div[@class='col-lg-6 auth-form']//h3"))
        )
        return element.is_displayed() and element.text == "Login"

    def registration_error_is_displayed(self):
        element = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "app-register form.ng-dirty.ng-touched.ng-valid.ng-submitted .alert.alert-danger .help-block"))
        )
        return element.is_displayed()


    def go_to_login_page(self):
        return WebDriverUtils(driver=self.driver)\
            .click_by_css_selector(css_selector='a[data-test="nav-sign-in"]')

    def register_from_login_page(self,
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
        dob = dob or self.generate_random_date_of_birth()
        web_driver_utils = web_driver_utils or WebDriverUtils(driver=self.driver)

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


    def test_user_registration(self):
        web_driver_utils = self.go_to_login_page()
        self.register_from_login_page(web_driver_utils=web_driver_utils)
        assert self.login_page_is_displayed(), "User is not on the login page after submission."


    def test_duplicate_email_registration(self):
        email = Faker().email()
        web_driver_utils = self.go_to_login_page()
        self.register_from_login_page(web_driver_utils=web_driver_utils, email=email)
        assert self.login_page_is_displayed(), "User is not on the login page after submission."

        self.register_from_login_page(web_driver_utils=web_driver_utils, email=email)
        assert self.registration_error_is_displayed(), "Somehow the user was able to register with used email"


    def test_not_valid_dob(self):
        web_driver_utils = self.go_to_login_page()
        self.register_from_login_page(web_driver_utils=web_driver_utils, dob=self.generate_random_date_of_birth(min_age=10, max_age=11))
        assert self.registration_error_is_displayed(), "User is too young to register an account."


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
