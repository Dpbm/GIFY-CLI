from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
from utils.remove_duplicates_from_list import remove_duplicates
from utils.check_if_page_has_been_loaded import page_has_loaded
from prettytable import PrettyTable
from time import sleep
from yaspin import yaspin
from yaspin.spinners import Spinners
import emoji 
import sys
import asyncio

from constants import *

from stages.browse_directory import browse_directory
from stages.check_input import check_input_args
from stages.get_links import get_links
from stages.get_title import get_title
from stages.get_views import get_views
from stages.get_date import get_date
from stages.get_likes_and_dislikes import get_likes_and_dislikes
from stages.get_amount_of_comments import get_amount_of_comments
from stages.create_xlsx import create_xlsx
from stages.get_page import get_page

async def main():
    try:
        table = PrettyTable(OUTPUT_PRINT_HEADER)

        await check_input_args(sys.argv)

        URL = sys.argv[1]
        OUTPUT_FILE_NAME = sys.argv[2]

        directory = ""
        while not directory:
            directory = await browse_directory()

        print(emoji.emojize(f'{colors.CYAN}:open_file_folder:   Selected Directory: {directory}'))

        browser, soup = await get_page(URL)

        with yaspin(Spinners.moon, text=f"{colors.HEADER}Getting Links"):
            links = await get_links(soup)
            
        print(emoji.emojize(f"{colors.GREEN}\n\n:check_mark: Links\n"))

        links = remove_duplicates(links)

        titles = []
        visualizations = []
        dates = []
        likes = []
        dislikes = []
        comments = []


        for link in links:
            
            browser.get(link)
            await page_has_loaded(browser)
            sleep(1.4)

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            title = await get_title(soup)
            titles.append(title)

            header = title.center(100, f'_')
            print(f'{colors.HEADER}{header}')
            print(emoji.emojize(f"{colors.GREEN}:check_mark: Title"))


            visualization = await get_views(browser)
            visualizations.append(visualization) 
            print(emoji.emojize(f"{colors.GREEN}:check_mark: Visualizations"))

            date = await get_date(browser)
            dates.append(date)
            print(emoji.emojize(f"{colors.GREEN}:check_mark: Date"))



            likes_in_video, dislikes_in_video = await get_likes_and_dislikes(browser)
            likes.append(likes_in_video)
            print(emoji.emojize(f"{colors.GREEN}:check_mark: Likes"))
            dislikes.append(dislikes_in_video)
            print(emoji.emojize(f"{colors.GREEN}:check_mark: Deslikes"))

            
            controller = 10
            with yaspin(Spinners.runner, text=f"{colors.HEADER}Getting Amount of Comments") as sp:
                amount_of_comments = await get_amount_of_comments(browser)
                comments.append(amount_of_comments)

                sp.text = f'{colors.GREEN}Comments amount'
                sp.green.ok("✔")
            
            table.add_row([title, visualization, date, likes_in_video, dislikes_in_video, amount_of_comments, link])
            print('\n\n')

        finish = f"{colors.HEADER}Output"
        finish = finish.center(100, '-')
        print(f'{colors.HEADER}{finish}')
        print(table)

        browser.quit()

        with yaspin(Spinners.moon, text=f"{colors.HEADER}Making xlsx file") as sp:
            await create_xlsx(titles, visualizations, dates, likes, dislikes, comments, links, directory, OUTPUT_FILE_NAME)
            sp.text = f'{colors.GREEN}DONE'
            sp.green.ok("✔")

    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    asyncio.run(main())