import time

from selenium.webdriver.support import expected_conditions as ec
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


fake = Faker()

def add_brand(web_driver_utils, name):
        go_to_brand(web_driver_utils)\
        .fill(xpath='//*[@id="name"]', value=name)\
        .fill(xpath='//*[@id="slug"]', value=name.lower()+"-slug")\
        .click(xpath='//div[@class="container mt-5"]//form//div[@class="row"][3]//div[@class="col-12"]//button')

def go_to_brand(web_driver_utils):
    web_driver_utils \
        .click(xpath='//*[@id="admin-menu"]') \
        .click(xpath="/html/body/app-root/app-header/nav/div/div/ul/li[4]/ul/li[2]/a") \
        .click(xpath="/html/body/app-root/div/app-list/form/div/a")
    return web_driver_utils

def brand_added(driver=None):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".alert-success"))
    )
    return element.is_displayed() and element.text=="Brand saved!"

def brand_duplicated(driver=None):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".alert-danger"))
    )
    return element.is_displayed() and element.text == "A brand already exists with this slug."