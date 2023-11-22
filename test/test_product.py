import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils import WebDriverUtils

class ExampleTest(unittest.TestCase):
    BASE_URL = "https://practicesoftwaretesting.com"

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def test_add_product(self):
        web_driver_utils = WebDriverUtils(self.driver)\
            .login_as_admin()\
            .click('//*[@id="admin-menu"]')\
            .click("/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")\
            .click("/html/body/app-root/div/app-products-list/form/div/a")\
            .fill('//*[@id="name"]', "Test Product")\
            .fill('//*[@id="description"]', "Test Product Description")\
            .fill('//*[@id="stock"]', "10")\
            .fill('//*[@id="price"]', "123.45")\
            .select_option('//*[@id="brand_id"]', 0)\
            .select_option('//*[@id="category_id"]', 0)\
            .select_option('//*[@id="product_image_id"]', 0)\
            .click('/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')\
            .click("/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/a")\
            .fill("/html/body/app-root/div/app-products-list/form/div/input", "Test Product")\
            .click_and_sleep( "/html/body/app-root/div/app-products-list/form/div/button[1]", 1)

        # The product is not added, due to a bug in the application.
        self.assertTrue(
            web_driver_utils.is_value_in_element_text(
                "/html/body/app-root/div/app-products-list/table",
                "Test Product"
            )
        )

    def test_edit_product_with_negative_price(self):
        web_driver_utils = WebDriverUtils(self.driver)\
            .login_as_admin()\
            .click('//*[@id="admin-menu"]')\
            .click("/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")

        product_id = web_driver_utils.get_element_text("/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[1]")

        web_driver_utils\
            .click_and_sleep("/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[5]/a", 2)\
            .fill('//*[@id="price"]', "-123.45")\
            .click('/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')\
            .click("/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/a")
        
        product_modified_price = web_driver_utils.get_element_text(f'//tr[td[text()="{product_id}"]]/td[4]')

        self.assertEqual("$14.15", product_modified_price)

        # Restore original price to prevent the next test failure
        web_driver_utils.click_and_sleep("/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[5]/a", 2)\
            .fill('//*[@id="price"]', "14.15")\
            .click('/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')

    def test_display_product_details(self):
        web_driver_utils = WebDriverUtils(self.driver)\
            .login_as_admin()\
            .click('//*[@id="admin-menu"]')\
            .click("/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")\
            .fill("/html/body/app-root/div/app-products-list/form/div/input", "Slip Joint Pliers")\
            .click("/html/body/app-root/div/app-products-list/form/div/button[1]")

        base_xpath = "/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td"
        name = web_driver_utils.get_element_text(f"{base_xpath}[2]")
        stock = web_driver_utils.get_element_text(f"{base_xpath}[3]")
        price = web_driver_utils.get_element_text(f"{base_xpath}[4]")

        # Validate product details
        self.assertEqual("Slip Joint Pliers", name)
        self.assertEqual("11", stock)
        self.assertEqual("$9.17", price)

    def test_display_empty_product_list(self):
        web_driver_utils = WebDriverUtils(self.driver)\
            .login_as_admin()\
            .click('//*[@id="admin-menu"]')\
            .click("/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")\
            .fill("/html/body/app-root/div/app-products-list/form/div/input", "Non Existing Product")\
            .click("/html/body/app-root/div/app-products-list/form/div/button[1]")

        # Validate product details
        self.assertFalse(
            web_driver_utils.is_value_in_element_text(
                "/html/body/app-root/div/app-products-list/table",
                "Non Existing Product"
            )
        )

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
