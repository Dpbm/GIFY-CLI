from utils.convert_list_to_string import convert

async def get_title(page):
    title = page.title.string.split()[:-2]
    title = convert(title)

    return title