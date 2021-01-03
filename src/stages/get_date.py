from selenium import webdriver
from constants import XPATH_DATE

async def get_date(browser):
    getDate = browser.find_element_by_xpath(XPATH_DATE)
    date = getDate.get_attribute('innerText')
    return date