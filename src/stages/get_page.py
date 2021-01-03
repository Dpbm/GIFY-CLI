from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

async def get_page(URL):
    option = Options()
    option.add_argument ('--headless')  
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    return browser, soup