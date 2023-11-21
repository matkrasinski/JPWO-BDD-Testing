import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils import login_as_admin, click, fill, select_option, is_value_in_element_text, get_element_text


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
        login_as_admin(self.driver)

        # Go to products page
        click(self.driver, '//*[@id="admin-menu"]')
        click(self.driver, "/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")
        click(self.driver, "/html/body/app-root/div/app-products-list/form/div/a")

        # Add a new product details
        fill(self.driver, '//*[@id="name"]', "Test Product")
        fill(self.driver, '//*[@id="description"]', "Test Product Description")
        fill(self.driver, '//*[@id="stock"]', "10")
        fill(self.driver, '//*[@id="price"]', "123.45")
        select_option(self.driver, '//*[@id="brand_id"]', 0)
        select_option(self.driver, '//*[@id="category_id"]', 0)
        select_option(self.driver, '//*[@id="product_image_id"]', 0)

        # Save the product and go back
        click(self.driver, '/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')
        click(self.driver, "/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/a")

        # Search for created product
        fill(self.driver, "/html/body/app-root/div/app-products-list/form/div/input", "Test Product")
        click(self.driver, "/html/body/app-root/div/app-products-list/form/div/button[1]")
        sleep(1)

        # The product is not added, due to a bug in the application.
        self.assertTrue(
            is_value_in_element_text(
                self.driver,
                "/html/body/app-root/div/app-products-list/table",
                "Test Product"
            )
        )

    def test_edit_product_with_negative_price(self):
        login_as_admin(self.driver)

        # Go to products page
        click(self.driver, '//*[@id="admin-menu"]')
        click(self.driver, "/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")

        # Edit first product from the list
        product_id = get_element_text(self.driver, "/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[1]")

        click(self.driver, "/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td[5]/a")
        sleep(2)  # Wait for the page to load
        fill(self.driver, '//*[@id="price"]', "-123.45")

        # Save the product
        click(self.driver, '/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/button')

        # Check if the product price is modified
        click(self.driver, "/html/body/app-root/div/app-products-add-edit/div/form/div[3]/div/a")
        product_modified_price = get_element_text(self.driver, f'//tr[td[text()="{product_id}"]]/td[4]')

        # Product can have negative price, due to a bug in the application.
        self.assertEqual("$14.15", product_modified_price)

    def test_display_product_details(self):
        login_as_admin(self.driver)

        # Go to products page
        click(self.driver, '//*[@id="admin-menu"]')
        click(self.driver, "/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[4]/a")

        # Search for product
        fill(self.driver, "/html/body/app-root/div/app-products-list/form/div/input", "Slip Joint Pliers")
        click(self.driver, "/html/body/app-root/div/app-products-list/form/div/button[1]")

        # Get product details
        base_xpath = "/html/body/app-root/div/app-products-list/table/tbody/tr[1]/td"
        id = get_element_text(self.driver, f"{base_xpath}[1]")
        name = get_element_text(self.driver, f"{base_xpath}[2]")
        stock = get_element_text(self.driver, f"{base_xpath}[3]")
        price = get_element_text(self.driver, f"{base_xpath}[4]")

        # Validate product details
        self.assertEqual("01HFSYBMY5XX9TM48Z34R1MV7E", id)
        self.assertEqual("Slip Joint Pliers", name)
        self.assertEqual("11", stock)
        self.assertEqual("$9.17", price)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
