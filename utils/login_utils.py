from utils.web_driver_utils import WebDriverUtils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def login(web_driver_utils=None, driver=None, email="", password=""):
    web_driver_utils = web_driver_utils or WebDriverUtils(driver=driver)
    web_driver_utils\
        .fill(xpath='//*[@id="email"]', value=email)\
        .fill_and_press_return(xpath='//*[@id="password"]', value=password)


def go_to_profile(web_driver_utils=None, driver=None):
    web_driver_utils = web_driver_utils or WebDriverUtils(driver=driver)
    web_driver_utils\
        .click(xpath="//app-overview//a[@class='btn btn-outline-secondary d-flex justify-content-start align-items-center'][2]")


def change_password(web_driver_utils=None, driver=None, curr_password=None, new_password=None, conf_new_password=None):
    web_driver_utils = web_driver_utils or WebDriverUtils(driver=driver)
    web_driver_utils\
        .fill(xpath='//*[@id="current-password"]', value=curr_password)\
        .fill(xpath='//*[@id="new-password"]', value=new_password)\
        .fill_and_press_return(xpath='//*[@id="new-password-confirm"]', value=conf_new_password)
    

def password_change_error_is_displayed(driver=None):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "/html/body/app-root/div[@class='container']/app-profile/div[@class='container mt-5']/form[@class='ng-dirty ng-touched ng-valid ng-submitted']/div[@class='row'][2]/div[@class='col-12']/div[@class='alert alert-danger mt-3']"))
    )
    return element.is_displayed() 
    
