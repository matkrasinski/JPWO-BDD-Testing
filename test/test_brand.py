import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.brand_utils import add_brand, brand_added, brand_duplicated
from utils.category_utils import category_added, add_category, category_duplicated

from faker import Faker

from utils.web_driver_utils import WebDriverUtils


class BrandTest(unittest.TestCase):

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

    def test_add_brand(self):
        fake=Faker()
        name=fake.first_name()
        web_driver_utils = WebDriverUtils(driver=self.driver) \
            .login_as_admin()
        add_brand( web_driver_utils=web_driver_utils, name=name)
        assert brand_added(driver=self.driver)


    def test_category_duplicated(self):
        fake=Faker()
        name = fake.first_name()
        web_driver_utils = WebDriverUtils(driver=self.driver) \
            .login_as_admin()
        add_brand(web_driver_utils=web_driver_utils, name=name)
        add_brand(web_driver_utils=web_driver_utils, name=name)
        assert brand_duplicated(driver=self.driver)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

