import re
import csv


import aiohttp
import asyncio


import requests
from bs4 import BeautifulSoup



def clear_string(string):  # В основном только для того, что удать знак "рубль" из строки "цена"
    return re.sub('\D', '', string)


def get_normalized_page_url(url_to_normalize):
    if '?' in url_to_normalize:
        return '-'.join(url_to_normalize.split('?')[:-1])
    else:
        return url_to_normalize


def write_csv(data):
    with open('result.csv', 'a') as f:
        fields = ['full_name', 'brand', 'current_price', 'default_price'] #  , 'url'
        writer = csv.DictWriter(f, fieldnames=fields)
        for product in data:
            writer.writerow(product)


def get_total_page(url):
    """
        Фукнция в тупую берет максимальное коль-во страниц с выбранным товаром и начинает считать кол-во страниц
    """
    s = requests.Session()
    get_page = s.get(url+'?page=1')
    page_count = 0
    if 'pagination-next' in get_page.text:
        i = 1
        while i <= 5000:
            get_next_page = s.get(url + '?page={}'.format(i))
            page_count += 1
            i += 1

            if 'dtList-inner' not in get_next_page.text:
                break

        return page_count - 1
    else:
        page_count = 1
        return page_count


def parse_all_product_link(url, page_count):
    base_url = 'https://www.wildberries.ru'
    products_link = []
    """
        - Функция работает с базовым урлом на страницу с нужными товарами + {page}
        - Коротко говоря, просто считает сколько страниц с выбранным товаром есть
    """
    s = requests.Session()

    if page_count > 1:
        for i in range(1, page_count + 1):

            html = s.get(url + f'?page={i}')
            soup = BeautifulSoup(html.text, 'lxml')
            all_product_link = soup.find_all('div', {'class': 'dtList-inner'})
            for k in all_product_link:
                products_link.append(base_url + k.span.span.a.get('href'))

        print(products_link)
        return products_link
    else:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        all_product_link = soup.find_all('div', {'class': 'dtList-inner'})
        for i in all_product_link:
            products_link.append(base_url + i.span.span.a.get('href'))

        return products_link


products_data = []


async def parse_selected_product_data(product_url):
    """
    Функция скрапинга информации о товаре
    Переходим по ссылке - парсим данные - записываем в cловарь
    """

    soup = BeautifulSoup(product_url, 'lxml')
    product_detailt_page = soup.find_all('div', {'class': 'product-content-v1'})

    for child in product_detailt_page:
        try:
            full_name = child.find(class_='brand-and-name').get_text().strip().encode('ascii', 'ignore').decode(encoding="utf-8")
        except:
            full_name = ''
        try:
            brand = child.find(class_='brand').get_text().strip().encode('ascii', 'ignore').decode(encoding="utf-8")
        except:
            brand = ''
        try:
            current_price = child.find(class_='final-cost').get_text().strip().encode('ascii', 'ignore').decode(encoding="utf-8")
        except:
            current_price = ''
        try:
            default_price = child.find(class_='c-text-base').get_text().strip().encode('ascii', 'ignore').decode(encoding="utf-8")
        except:
            default_price = ''
        data = {'full_name': full_name, 'brand': brand, 'current_price': current_price, 'default_price': default_price
                } #'url': base_url + product_url
        products_data.append(data)

        print(data)



def parse_inner_products_data(url_list):
    """
        Получаем лист с ссылками на детальную инфу о товаре и отсюда вызваем функции скрапинга для каждого товара
    """
    product_data = []
    for i in url_list:
        data = parse_selected_product_data(i)
        product_data.append(data)

    return product_data


def make_request(urls):
    parse_selected_product_data(urls)


