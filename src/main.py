from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
from utils.remove_duplicates_from_list import remove_duplicates
from utils.check_if_page_has_been_loaded import page_has_loaded
from utils.convert_list_to_string import convert
from webdriver_manager.chrome import ChromeDriverManager
from prettytable import PrettyTable
from time import sleep
from yaspin import yaspin
from yaspin.spinners import Spinners
import emoji 
import sys
from tkinter import *
from tkinter import filedialog 
import asyncio
import xlsxwriter

async def browse_files(): 
    root = Tk()
    root.option_add('*foreground', 'black')  
    root.option_add('*activeForeground', 'black')
    root.withdraw()
    dir_name = filedialog.askdirectory() 
    return dir_name
       
       
async def main():
    PREFIX = 'https://www.youtube.com'

    table = PrettyTable(['title', 'visualizations', 'date', 'likes in video', 'deslikes in video', 'amount comments in video', 'links'])

    option = Options()
    option.add_argument ('--headless')  

    if len(sys.argv) - 1 > 2 or len(sys.argv) - 1 < 2:
        print("Usage: python src/main.py link output_file_name\n\n")
        print("You need to pass only two arguments")
        exit(1)

    url = sys.argv[1]
    out_file_name = sys.argv[2]
    directory = await browse_files()

    print(emoji.emojize(f':open_file_folder:   Selected Directory: {directory}'))

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    links = []

    with yaspin(Spinners.moon, text="Getting Links"):
        for link in soup.find_all('a'):
            if 'watch' in str(link.get('href')) and '&index=' in str(link.get('href')):
                links.append(PREFIX + link.get('href'))

    print(emoji.emojize("\n\n:check_mark: Links\n"))


    links = remove_duplicates(links)


    titles = []
    visualizations = []
    dates = []
    likes = []
    deslikes = []
    comments = []


    for link in links:
        browser.get(link)
        page_has_loaded(browser)
        sleep(5)

        soup = BeautifulSoup(browser.page_source, 'html.parser')
        title = soup.title.string.split()[:-2]
        title = convert(title)
        titles.append(title)
        header = title.center(100, '-')
        print(header)
        print(emoji.emojize(":check_mark: Title"))

        getVisualization = browser.find_element_by_xpath("//div[@id='info'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='info-text'][@class='style-scope ytd-video-primary-info-renderer']//div[@id='count'][@class='style-scope ytd-video-primary-info-renderer']//yt-view-count-renderer[@class='style-scope ytd-video-primary-info-renderer']//span[@class='view-count style-scope yt-view-count-renderer']")
        visualization = getVisualization.get_attribute('innerText').split()[0]
        visualizations.append(int(visualization.replace('.', ''))) 
        print(emoji.emojize(":check_mark: Visualizations"))


        getDate = browser.find_element_by_xpath("//*[@id='date']/yt-formatted-string")
        date = getDate.get_attribute('innerText')
        dates.append(date)
        print(emoji.emojize(":check_mark: Date"))



        get_likes_and_dislikes = browser.find_element_by_xpath("//div[@id='info']//div[@id='info-contents']//ytd-video-primary-info-renderer//div[@id='container']//div[@id='info']//div[@id='menu-container']//ytd-sentiment-bar-renderer//paper-tooltip//div[@id='tooltip']")
        likes_and_deslikes_in_video = get_likes_and_dislikes.get_attribute('innerText').split()
        likes_in_video = likes_and_deslikes_in_video[0]
        deslikes_in_video = likes_and_deslikes_in_video[-1]
        likes.append(int(likes_in_video.replace('.', '')))
        print(emoji.emojize(":check_mark: Likes"))
        deslikes.append(int(deslikes_in_video.replace('.', '')))
        print(emoji.emojize(":check_mark: Deslikes"))

        
        controller = 10
        spinner_comments = yaspin(Spinners.earth, text="getting Comments")


        with yaspin(Spinners.runner, text="Getting Comments") as sp:
            while True:
                browser.execute_script("window.scrollTo(0, {});".format(controller))
                sleep(0.3)
                try:
                    get_amount_of_comments = browser.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string")
                    amount_of_comments = get_amount_of_comments.get_attribute('innerText').split()[0]
                    comments.append(int(amount_of_comments.replace('.', '')))
                    sp.text = 'Comments amount'
                    sp.ok("✔")
                    break
                except Exception as error:
                    pass
                controller += 10
        
            
        
        table.add_row([title, visualization, date, likes_in_video, deslikes_in_video, amount_of_comments, link])
        print('\n\n')

    finish = "Output"
    finish = finish.center(100, '-')
    print(finish)
    print(table)

    browser.quit()

    with yaspin(Spinners.moon, text="Making xlsx file") as sp:
        output = xlsxwriter.Workbook(f'{os.path.join(directory, out_file_name)}.xlsx')
        worksheet = output.add_worksheet()
        
        
        header = {
            "A" : "Title",
            "B" : "Visualizations",
            "C" : "Date",
            "D" : "Likes in video",
            "E" : "Deslikes in Video",
            "F" : "Amount of comments",
            "G" : "Link"
        }
        
        for i in header.keys():
            worksheet.write(f'{i}1', header[i])
        

        for i in range(len(links)):
            worksheet.write(f'A{i+2}', titles[i])
            worksheet.write(f'B{i+2}', visualizations[i])
            worksheet.write(f'C{i+2}', dates[i])
            worksheet.write(f'D{i+2}', likes[i])
            worksheet.write(f'E{i+2}', deslikes[i])
            worksheet.write(f'F{i+2}', comments[i])
            worksheet.write(f'G{i+2}', links[i])

        worksheet.write_formula(f'B{len(links)+2}', '{=SUM(B2:B%i)}'%(len(links)+1))
        worksheet.write_formula(f'D{len(likes)+2}', '{=SUM(D2:D%i)}'%(len(likes)+1))
        worksheet.write_formula(f'E{len(deslikes)+2}', '{=SUM(E2:E%i)}'%(len(deslikes)+1))
        worksheet.write_formula(f'F{len(comments)+2}', '{=SUM(F2:F%i)}'%(len(comments)+1))



        output.close()
        
        sp.text = 'DONE'
        sp.ok("✔")




if __name__ == '__main__':
    asyncio.run(main())