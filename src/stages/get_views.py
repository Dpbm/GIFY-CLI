from selenium import webdriver
from constants import XPATH_VIEWS

async def get_views(browser):
    getVisualization = browser.find_element_by_xpath(XPATH_VIEWS)
    visualization = getVisualization.get_attribute('innerText').split()[0]
    return int(visualization.replace('.', ''))