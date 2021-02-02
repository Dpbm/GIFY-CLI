PREFIX = 'https://www.youtube.com'
OUTPUT_PRINT_HEADER = ['title', 'visualizations', 'date', 'likes in video', 'dislikes in video', 'amount comments in video', 'links']

XPATH_VIEWS = "//div[@id='info'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='info-text'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='count'][@class='style-scope ytd-video-primary-info-renderer']//yt-view-count-renderer[@class='style-scope ytd-video-primary-info-renderer']//span[@class='view-count style-scope yt-view-count-renderer']"
XPATH_DATE = "//*[@id='date']/yt-formatted-string"
XPATH_LIKES_AND_DISLIKES = "//div[@id='info']//div[@id='info-contents']//ytd-video-primary-info-renderer//div[@id='container']//div[@id='info']//div[@id='menu-container']//ytd-sentiment-bar-renderer//paper-tooltip//div[@id='tooltip']"
XPATH_AMOUNT_COMMENTS = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string"
XPATH_NO_COMMENTS = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-message-renderer/yt-formatted-string[1]/span"

class colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'