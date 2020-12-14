from time import sleep
from selenium import webdriver
from yaspin import yaspin
from yaspin.spinners import Spinners

def page_has_loaded(driver, sleep_time = 2):
    '''
    Waits for page to completely load by comparing current page hash values.
    made by: SoRobby
    link to: https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python 
    '''

    def get_page_hash(driver):
        '''
        Returns html dom hash
        '''
        # can find element by either 'html' tag or by the html 'root' id
        dom = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        dom_hash = hash(dom.encode('utf-8'))
        return dom_hash

    page_hash = 'empty'
    page_hash_new = ''
    
    # comparing old and new page DOM hash together to verify the page is fully loaded
    while page_hash != page_hash_new: 
        with yaspin(Spinners.clock, text="Waiting for load page") as spinner:
            sleep(2)  # time consuming code
            page_hash = get_page_hash(driver)
            sleep(sleep_time)
            page_hash_new = get_page_hash(driver)
