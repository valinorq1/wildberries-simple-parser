import datetime
import concurrent.futures

from utils import (get_normalized_page_url, get_total_page, parse_all_product_link, parse_inner_products_data,
                   write_csv, make_request, products_data)


def main(url_to_parse):
    url = get_normalized_page_url(url_to_parse)  # приводим ссылку к нормальному виду
    total_page = get_total_page(url)  # считаем кол-во страниц
    all_product_link = parse_all_product_link(url, total_page)  # получаем ссылки на внутренние страницы продуктов
    start = datetime.datetime.now()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(make_request, all_product_link)
    write_csv(products_data)  # пишем данные в csv
    end = datetime.datetime.now()
    print(f' Finished. \n Check Result.csv \n time taken {end-start}')


if __name__ == '__main__':
    url = 'https://www.wildberries.ru/catalog/dlya-remonta/elektroinstrumenty/payalno-termicheskie-instrumenty'
    main(url)
