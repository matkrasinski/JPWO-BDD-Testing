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
        web_driver_utils = WebDriverUtils(driver=self.driver)\
            .login_as_admin()\
            .click(xpath='//*[@id="admin-menu"]')\
            .click(xpath="/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")\
            .click(xpath="/html/body/app-root/div/app-products-list/form/div/a")\
            .fill(xpath='//*[@id="name"]', value="Test Product")\
            .fill(xpath='//*[@id="description"]', value="Test Product Description")\
            .fill(xpath='//*[@id="stock"]', value="10")\
            .fill(xpath='//*[@id="price"]', value="123.45")\
            .select_option(xpath='//*[@id="brand_id"]', index=0)\
            .select_option(xpath='//*[@id="category_id"]', index=0)\
            .select_option(xpath='//*[@id="product_image_id"]', index=0)\
            .click(xpath='/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')\
            .click(xpath="/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/a")\
            .fill(xpath="/html/body/app-root/div/app-products-list/form/div/input", value="Test Product")\
            .click_and_sleep(xpath="/html/body/app-root/div/app-products-list/form/div/button[1]", seconds=1)

        # The product is not added, due to a bug in the application.
        self.assertTrue(
            web_driver_utils.is_value_in_element_text(
                "/html/body/app-root/div/app-products-list/table",
                "Test Product"
            )
        )

    def test_edit_product_with_negative_price(self):
        web_driver_utils = WebDriverUtils(driver=self.driver)\
            .login_as_admin()\
            .click(xpath='//*[@id="admin-menu"]')\
            .click(xpath="/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")

        product_id = web_driver_utils.get_element_text("/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[1]")

        web_driver_utils\
            .click_and_sleep(xpath="/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[5]/a", seconds=2)\
            .fill(xpath='//*[@id="price"]', value="-123.45")\
            .click(xpath='/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')\
            .click(xpath="/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/a")
        
        product_modified_price = web_driver_utils.get_element_text(xpath=f'//tr[td[text()="{product_id}"]]/td[4]')

        self.assertEqual("$14.15", product_modified_price)

        # Restore original price to prevent the next test failure
        web_driver_utils.click_and_sleep(xpath="/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[5]/a", seconds=2)\
            .fill(xpath='//*[@id="price"]', value="14.15")\
            .click(xpath='/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')

    def test_display_product_details(self):
        web_driver_utils = WebDriverUtils(driver=self.driver)\
            .login_as_admin()\
            .click(xpath='//*[@id="admin-menu"]')\
            .click(xpath="/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")\
            .fill(xpath="/html/body/app-root/div/app-products-list/form/div/input", value="Slip Joint Pliers")\
            .click(xpath="/html/body/app-root/div/app-products-list/form/div/button[1]")

        base_xpath = "/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td"
        name = web_driver_utils.get_element_text(xpath=f"{base_xpath}[2]")
        stock = web_driver_utils.get_element_text(xpath=f"{base_xpath}[3]")
        price = web_driver_utils.get_element_text(xpath=f"{base_xpath}[4]")

        # Validate product details
        self.assertEqual("Slip Joint Pliers", name)
        self.assertEqual("11", stock)
        self.assertEqual("$9.17", price)

    def test_display_empty_product_list(self):
        web_driver_utils = WebDriverUtils(driver=self.driver)\
            .login_as_admin()\
            .click(xpath='//*[@id="admin-menu"]')\
            .click(xpath="/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")\
            .fill(xpath="/html/body/app-root/div/app-products-list/form/div/input", value="Non Existing Product")\
            .click(xpath="/html/body/app-root/div/app-products-list/form/div/button[1]")

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
