from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from time import sleep
from pathlib import Path
from utils.remove_duplicates_from_list import remove_duplicates
from utils.check_if_page_has_been_loaded import page_has_loaded
from utils.convert_list_to_string import convert


PREFIX = 'https://www.youtube.com'

DRIVER_PATH = Path('drivers', 'chrome', 'chromedriver')


DRIVER = DRIVER_PATH

option = Options()
option.add_argument ('--headless')


url = input('link: ')
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
dates = []
likes = []
deslikes = []

print(links)
for link in links:
    browser.get(link)
    page_has_loaded(browser)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    title = soup.title.string.split()[:-2]
    title = convert(title)
    titles.append(title)

    getVisualization = browser.find_element_by_xpath("//div[@id='info'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='info-text'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='count'][@class='style-scope ytd-video-primary-info-renderer']//yt-view-count-renderer[@class='style-scope ytd-video-primary-info-renderer']//span[@class='view-count style-scope yt-view-count-renderer']")
    visualization = getVisualization.get_attribute('innerText').split()[0]
    visualizations.append(visualization) 

    getDate = browser.find_element_by_xpath("//*[@id='date']/yt-formatted-string")
    date = getDate.get_attribute('innerText')
    dates.append(date)


    get_likes_and_dislikes = browser.find_element_by_xpath("//div[@id='info']//div[@id='info-contents']//ytd-video-primary-info-renderer//div[@id='container']//div[@id='info']//div[@id='menu-container']//ytd-sentiment-bar-renderer//paper-tooltip//div[@id='tooltip']")
    likes_and_deslikes_in_video = get_likes_and_dislikes.get_attribute('innerText').split()
    likes_in_video = likes_and_deslikes_in_video[0]
    deslikes_in_video = likes_and_deslikes_in_video[-1]
    likes.append(likes_in_video)
    deslikes.append(deslikes_in_video)

    get_amount_comments_in_video = browser.find_element_by_xpath("//ytd-comments[@id='comments']//ytd-item-section-renderer[@id='sections']//div[@id='header']")
    print(get_amount_comments_in_video)
    amount_comments_in_video = get_amount_comments_in_video.get_attribute('innerText')



    print(visualization, title, date, likes_in_video, deslikes_in_video, amount_comments_in_video)
    

browser.quit()