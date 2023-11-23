import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from faker import Faker
from utils.registration_utils import go_to_login_page, register_from_login_page, login_page_is_displayed 
from utils.login_utils import login, go_to_profile, change_password, password_change_error_is_displayed


class PasswordChangeTest(unittest.TestCase):
    
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

        
        self.email = Faker().email()
        self.password = Faker().password()

        self.web_driver_utils = go_to_login_page(driver=self.driver)
        register_from_login_page(driver=self.driver, web_driver_utils=self.web_driver_utils, email=self.email, password=self.password)
        login(driver=self.driver, web_driver_utils=self.web_driver_utils, email=self.email, password=self.password)
        go_to_profile(driver=self.driver, web_driver_utils=self.web_driver_utils)
        

    def test_change_password_success(self):
        new_password = Faker().password()
        conf_new_password = new_password
        change_password(driver=self.driver, web_driver_utils=self.web_driver_utils, curr_password=self.password, new_password=new_password, conf_new_password=conf_new_password)    
        assert login_page_is_displayed, "Something went wrong during changing the password"


    def test_change_password_incorrect_curr_password(self):
        new_password = Faker().password()
        conf_new_password = new_password
        change_password(driver=self.driver, web_driver_utils=self.web_driver_utils, curr_password=self.password + "_123", new_password=new_password, conf_new_password=conf_new_password)    
        assert password_change_error_is_displayed(driver=self.driver), "Error is not displayed"


    def test_change_password_incorrect_password_confirmation(self):
        new_password = Faker().password()
        conf_new_password = new_password + "_123"  
        change_password(driver=self.driver, web_driver_utils=self.web_driver_utils, curr_password=self.password, new_password=new_password, conf_new_password=conf_new_password)    
        assert password_change_error_is_displayed(driver=self.driver), "Error is not displayed"


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
