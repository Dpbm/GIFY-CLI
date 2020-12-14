from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from pathlib import Path
from utils.remove_duplicates_from_list import remove_duplicates
from utils.check_if_page_has_been_loaded import page_has_loaded
from utils.convert_list_to_string import convert
from webdriver_manager.chrome import ChromeDriverManager
from prettytable import PrettyTable
from time import sleep
from yaspin import yaspin
from yaspin.spinners import Spinners
import emoji

PREFIX = 'https://www.youtube.com'

table = PrettyTable(['title', 'visualizations', 'date', 'likes in video', 'deslikes in video', 'amount comments in video'])

option = Options()
option.add_argument ('--headless')  


url = input('link: ')
file_name = input('output file name: ')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'html.parser')

links = []

with yaspin(Spinners.moon, text="Getting Links"):
    for link in soup.find_all('a'):
        if 'watch' in str(link.get('href')) and '&index=' in str(link.get('href')):
            links.append(PREFIX + link.get('href'))

print(emoji.emojize(":check_mark: Links"))


links = remove_duplicates(links)


titles = []
visualizations = []
dates = []
likes = []
deslikes = []


for link in links:
    browser.get(link)
    page_has_loaded(browser)
    sleep(5)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    title = soup.title.string.split()[:-2]
    title = convert(title)
    titles.append(title)
    print()
    print(emoji.emojize(":check_mark: Title"))

    getVisualization = browser.find_element_by_xpath("//div[@id='info'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='info-text'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='count'][@class='style-scope ytd-video-primary-info-renderer']//yt-view-count-renderer[@class='style-scope ytd-video-primary-info-renderer']//span[@class='view-count style-scope yt-view-count-renderer']")
    visualization = getVisualization.get_attribute('innerText').split()[0]
    visualizations.append(visualization) 
    print(emoji.emojize(":check_mark: Visualizations"))


    getDate = browser.find_element_by_xpath("//*[@id='date']/yt-formatted-string")
    date = getDate.get_attribute('innerText')
    dates.append(date)
    print(emoji.emojize(":check_mark: Date"))



    get_likes_and_dislikes = browser.find_element_by_xpath("//div[@id='info']//div[@id='info-contents']//ytd-video-primary-info-renderer//div[@id='container']//div[@id='info']//div[@id='menu-container']//ytd-sentiment-bar-renderer//paper-tooltip//div[@id='tooltip']")
    likes_and_deslikes_in_video = get_likes_and_dislikes.get_attribute('innerText').split()
    likes_in_video = likes_and_deslikes_in_video[0]
    deslikes_in_video = likes_and_deslikes_in_video[-1]
    likes.append(likes_in_video)
    print(emoji.emojize(":check_mark: Likes"))
    deslikes.append(deslikes_in_video)
    print(emoji.emojize(":check_mark: Deslikes"))

    
    controller = 10
    spinner_comments = yaspin(Spinners.earth, text="getting Comments")

    with yaspin(Spinners.earth, text="Getting Comments") as sp:
        while True:

            browser.execute_script("window.scrollTo(0, {});".format(controller))
            sleep(0.3)
            try:
                get_amount_of_comments = browser.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string")
                amount_of_comments = get_amount_of_comments.get_attribute('innerText').split()[0]
                print(emoji.emojize(":check_mark: Comments"))

                break
            except Exception as error:
                pass
            controller += 10
        sleep(0.3)
    
    table.add_row([title, visualization, date, likes_in_video, deslikes_in_video, amount_of_comments])
    print(table)
    

browser.quit()