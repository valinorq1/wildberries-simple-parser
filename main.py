import datetime


import asyncio
import aiohttp


from utils import *


async def fetch_content(url, session):
    async with session.get(url) as respone:
        product_html = await respone.text()
        await parse_selected_product_data(product_html)


async def main(url_to_parse):
    url = get_normalized_page_url(url_to_parse)  # приводим ссылку к нормальному виду
    total_page = get_total_page(url)  # считаем кол-во страниц
    all_product_link = parse_all_product_link(url, total_page) #  спарсили все ссылки на товары
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in all_product_link:
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    start = datetime.datetime.now()
    url_to_parse = "https://www.wildberries.ru/brands/adidas/krossovki"
    asyncio.run(main(url_to_parse))
    end = datetime.datetime.now()
    print('time taken:  ', end-start)
    write_csv(products_data)
