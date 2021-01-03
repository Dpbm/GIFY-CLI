from bs4 import BeautifulSoup
from constants import PREFIX

async def get_links(page):
    links = []
    for link in page.find_all('a'):
            if 'watch' in str(link.get('href')) and '&index=' in str(link.get('href')):
                links.append(PREFIX + link.get('href'))
    return links
