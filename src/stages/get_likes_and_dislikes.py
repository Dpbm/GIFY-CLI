from selenium import webdriver
from constants import XPATH_LIKES_AND_DISLIKES

async def get_likes_and_dislikes(browser):
    get_likes_and_dislikes = browser.find_element_by_xpath(XPATH_LIKES_AND_DISLIKES)
    likes_and_dislikes_in_video = get_likes_and_dislikes.get_attribute('innerText').split()
    likes_in_video = likes_and_dislikes_in_video[0]
    dislikes_in_video = likes_and_dislikes_in_video[-1]
    return int(likes_in_video.replace('.', '')), int(dislikes_in_video.replace('.', ''))