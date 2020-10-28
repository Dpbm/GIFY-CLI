from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from time import sleep

def remove_duplicates(list_of_elements):
    return list(dict.fromkeys(list_of_elements))

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
        # dom = driver.find_element_by_id('root').get_attribute('innerHTML')
        dom_hash = hash(dom.encode('utf-8'))
        return dom_hash

    page_hash = 'empty'
    page_hash_new = ''
    
    # comparing old and new page DOM hash together to verify the page is fully loaded
    while page_hash != page_hash_new: 
        page_hash = get_page_hash(driver)
        sleep(sleep_time)
        page_hash_new = get_page_hash(driver)




PREFIX = 'https://www.youtube.com'
DRIVER = '../drivers/chrome/chromedriver'

option = Options()
option.add_argument ('--headless')

url = 'https://www.youtube.com/playlist?list=PLRI3WTPj4rE0c0cfa3urcRuezzXDDYoa2'
browser = webdriver.Chrome(DRIVER, options=option)
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'html.parser')




links = []
for link in soup.find_all('a'):
    if 'watch' in str(link.get('href')) and '&index=' in str(link.get('href')):
        links.append(PREFIX + link.get('href'))

links = remove_duplicates(links)


titles = []
visualizations = []

print(links)
for link in links:
    browser.get(link)
    page_has_loaded(browser)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    title = soup.title.string.replace(' - YouTube', '')
    titles.append(title)

    getVisualization = browser.find_element_by_xpath("//div[@id='info'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='info-text'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='count'][@class='style-scope ytd-video-primary-info-renderer']//yt-view-count-renderer[@class='style-scope ytd-video-primary-info-renderer']//span[@class='view-count style-scope yt-view-count-renderer']")
    visualization = getVisualization.get_attribute('innerText').replace(' visualizações', '')
    visualizations.append(visualization) 

    

    print(visualization, title)
    

browser.quit()