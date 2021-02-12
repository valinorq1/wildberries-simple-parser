import datetime


from utils import get_normalized_page_url, get_total_page, parse_all_product_link, parse_inner_products_data, write_csv


def main(url_to_parse):
    url = get_normalized_page_url(url_to_parse)  # приводим ссылку к нормальному виду
    total_page = get_total_page(url)  # считаем кол-во страниц
    all_product_link = parse_all_product_link(url, total_page)  # получаем ссылки на внутренние страницы продуктов
    product_list = parse_inner_products_data(all_product_link)  # парсим данные с внутренних страниц
    write_csv(product_list)  # пишем данные в csv
    print('Finished. \n Check Result.csv')


if __name__ == '__main__':
    url = 'https://www.wildberries.ru/catalog/dlya-remonta/elektroinstrumenty/payalno-termicheskie-instrumenty'
    main(url)
