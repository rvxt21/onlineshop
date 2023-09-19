import re
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from anyascii import anyascii
import requests
from django.utils.text import slugify
from requests import Session
from http import HTTPStatus
from selectolax.parser import HTMLParser
from queue import Queue
from threading import Lock

# from shop.models import Image, Product, Category

lock = Lock()
logger = logging.getLogger(__name__)

excluded_links = {
    'https://tennismag.com.ua/info_green.png',
    'https://tennismag.com.ua/upload/alexkova.rklite/1bd/1bdc95770e91db9a83dca2c02ac8eb83.jpg',
    'https://tennismag.com.ua/upload/alexkova.rklite/448/4480cdc2141c1009062c71e496e1b84f.jpg',
    'https://tennismag.com.ua/ua/images/tennismag_logo.png',
    'https://tennismag.com.ua/upload/alexkova.rklite/321/321faad204f6838837d46fae9e1673bf.jpg',
    'https://tennismag.com.ua/upload/alexkova.rklite/1bd/1bdc95770e91db9a83dca2c02ac8eb83.jpg',
    'https://tennismag.com.ua/upload/alexkova.rklite/321/321faad204f6838837d46fae9e1673bf.jpg',
    'https://tennismag.com.ua/upload/alexkova.rklite/de9/de9f20a49b50901fd11d821ab4291466.jpg'
}


# def upload_images_to_local_media(images: list[str], product: Product) -> None:
#     for i, image in enumerate(images, start=1):
#         with requests.Session() as session:
#             response = session.get(image)
#             assert response.status_code == HTTPStatus.OK, 'Wrong status code'
#
#         with open(f'media/images/product/{product.slug}-{i}.jpg', 'wb') as file:
#             file.write(response.content)
#
#         Image.objects.create(
#             product=product,
#             image=f'images/product/{product.slug}-{i}.jpg',
#             url=image,
#         )


# def write_to_db(data: dict) -> Any:
#     product, _ = Product.objects.get_or_create(
#         slug=f"{slugify(anyascii(data['Title']))}-{data['Url'].split('/')[-1]}",
#         defaults={
#             'title': data['Title'],
#             'description': data['Description'][0]
#             if data['Description'] else None,
#             'price': data['Price'],
#             'old_price': data['Old price'],
#             'discount': data['Discount'],
#             'source_url': data['Url'],
#
#         }
#     )
#     for category in data['Categories']:
#         category, _ = Category.objects.get_or_create(
#             slug=slugify(anyascii(category)),
#             defaults={
#                 'name': category,
#             }
#         )
#         product.categories.add(category)
#
#     if data['Images']:
#         upload_images_to_local_media(data['Images'], product)
#
#     logger.warning('Product %s saved', product.slug)


def get_response_result(url: str) -> str:
    with Session() as session:
        response = session.get(url=url)
        assert response.status_code == HTTPStatus.OK

    return response.text


def parse_products_data(html_string: str, url: str) -> dict[str, Any]:
    tree = HTMLParser(html_string)
    name = tree.css_first('h1').text(strip=True)
    categories = tree.css('div.bx-breadcrumb-item span')
    categories = [c.text(strip=True) for c in categories[2:-1]]
    description = tree.css_first('div.bxr-detail-tab.bxr-detail-text')
    description = description.text(
        strip=True) if description else ''
    product_article = tree.css_first('div#art_number').text(strip=True)
    price = tree.css_first('span.bxr-market-current-price')
    if price:
        price = clean_price(price.text(strip=True))
    else:
        price = tree.css_first('span.bxr-market-current-price')
        price = clean_price(price.text(strip=True))
    old_price = tree.css_first('span.bxr-market-old-price')
    if old_price:
        old_price = clean_price(old_price.text(strip=True))
    else:
        old_price = None
    discount = None
    if old_price:
        discount = round((price / old_price) * 100 - 100, 2)
    characteristics = tree.css('.bxr-detail-tab td')
    characteristics = [characteristic.text(strip=True)
                       for characteristic in characteristics]
    characteristics = {characteristics[i]: characteristics[i + 1] for i in
                       range(0, len(characteristics), 2)}
    images = tree.css('a img')
    if images:
        image_links = [f'https://tennismag.com.ua{i.attributes["src"]}' for
                       i in images]
        images = {link.replace(".jpg", ".jpg ") for link in image_links
                  if link not in excluded_links}
    else:
        images = None
    return {
         'Title': name,
         'Categories': categories,
         'Description': description,
         'Characteristics': characteristics,
         'Price': price,
         'Product article': product_article,
         'Old price': old_price,
         'Discount': discount,
         'Images': images,
         'Url': url
    }


def clean_price(price: str) -> int | None:
    if not price:
        return None
    return int(re.sub(r'\D', '', price))//100


def test_collect_products_data(url: str) -> None:
    html_string = get_response_result(url)
    tree = HTMLParser(html_string)
    name = tree.css_first('h1').text(strip=True)
    categories = tree.css('div.bx-breadcrumb-item span')
    categories = [c.text(strip=True) for c in categories[2:-1]]
    description = tree.css_first('div.bxr-detail-tab.bxr-detail-text')
    description = description.text(
        strip=True) if description else ''
    product_article = tree.css_first('div#art_number').text(strip=True)
    price = tree.css_first('span.bxr-market-current-price')
    if price:
        price = clean_price(price.text(strip=True))
    else:
        price = tree.css_first('span.bxr-market-current-price')
        price = clean_price(price.text(strip=True))
    old_price = tree.css_first('span.bxr-market-old-price')
    if old_price:
        old_price = clean_price(old_price.text(strip=True))
    else:
        old_price = None
    discount = None
    if old_price:
        discount = round((price / old_price) * 100 - 100, 2)
    characteristics = tree.css('.bxr-detail-tab td')
    characteristics = [characteristic.text(strip=True)
                       for characteristic in characteristics]
    characteristics = {characteristics[i]: characteristics[i + 1] for i in
                 range(0, len(characteristics), 2)}
    images = tree.css('a img')
    if images:
        image_links = [f'https://tennismag.com.ua{i.attributes["src"]}' for
                       i in images]
        images = {link.replace(".jpg", ".jpg ") for link in image_links
                  if link not in excluded_links}
    else:
        images = None

    data = {
            'Title': name,
            'Categories': categories,
            'Description': description,
            'Characteristics': characteristics,
            'Price': price,
            'Product article': product_article,
            'Old price': old_price,
            'Discount': discount,
            'Images': images,
            'Url': url

        }
    print(data)


# def worker(qu: Queue, session: requests.Session) -> None:
#     while not qu.empty():
#         url = qu.get()
#         logger.info('Working on %s, queue size=%s', url, qu.qsize())
#         try:
#             response = session.get(url=url, timeout=10)
#             assert response.status_code == HTTPStatus.OK, 'Wrong status code'
#             data = parse_products_data(response.text, url)
#             with lock:
#                 write_to_db(data)
#         except (
#                 requests.exceptions.ConnectionError,
#                 requests.exceptions.ReadTimeout,
#                 requests.exceptions.Timeout,
#                 requests.exceptions.TooManyRedirects,
#                 requests.exceptions.RequestException,
#                 AssertionError,
#         ) as error:
#             logger.warning('%s, url %s', error, url)
#             qu.put(url)
#         except Exception as error:
#             logger.exception('Url %s %s', url, error)


def get_product_links_from_sitemap(url: str) -> list[str]:
    with requests.Session() as session:
        response = session.get(url=url)
        assert response.status_code == HTTPStatus.OK, 'Wrong status code'

    tree = HTMLParser(response.text)
    loc = tree.css('loc')

    return [elem.text(strip=True).replace('https://tennismag.com.ua/catalog/',
                                          'https://tennismag.com.ua/ua/catalog/'
                                          )
            for elem in loc
            if elem.text(strip=True).startswith(
                                            'https://tennismag.com.ua/catalog/'
                                                )
            ]


def main():
    # site_map_url = 'https://tennismag.com.ua/sitemap_iblock_10.xml'
    # product_links = get_product_links_from_sitemap(site_map_url)
    # logger.info('Number of products found %s', len(product_links))
    # session = requests.Session()
    # queue = Queue()
    # for link in product_links[1: 200]:
    #     queue.put(link)
    #
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     for _ in range(10):
    #         executor.submit(worker, queue, session)
    test_collect_products_data('https://tennismag.com.ua/ua/catalog/zhenskie-krossovki-nike/tennisnye-krossovki-nike-zoom-gp-turbo-hc-osaka/?offer=59242')

if __name__ == '__main__':
    main()