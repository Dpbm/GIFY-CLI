from time import sleep
from constants import XPATH_AMOUNT_COMMENTS

async def get_amount_of_comments(browser):
    controller = 10
    while True:
        browser.execute_script(f"window.scrollTo(0, {controller});")
        sleep(0.3)
        try:
            get_amount_of_comments = browser.find_element_by_xpath(XPATH_AMOUNT_COMMENTS)
            amount_of_comments = get_amount_of_comments.get_attribute('innerText').split()[0]
            break
        except Exception as error:
            pass
        controller += 10

    return int(amount_of_comments.replace('.', ''))