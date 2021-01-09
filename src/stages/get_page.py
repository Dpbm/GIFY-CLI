from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

async def get_page(URL):
    options = Options()
    options.add_argument ('--headless')   
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    return browser, soup