import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from utils.contact_utils import go_to_contact_page, fill_contact_form, generateMsg, message_is_send, \
    error_is_displayed

from faker import Faker


class ContactTest(unittest.TestCase):
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

    def test_contact_positive(self):
        web_driver_utils=go_to_contact_page(driver=self.driver)
        fill_contact_form(driver=self.driver, web_driver_utils=web_driver_utils, message=generateMsg())
        assert message_is_send(driver=self.driver)

    def test_contact_empty_message(self):
        web_driver_utils = go_to_contact_page(driver=self.driver)
        fill_contact_form(driver=self.driver, web_driver_utils=web_driver_utils, message=' ')
        assert error_is_displayed(driver=self.driver)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
