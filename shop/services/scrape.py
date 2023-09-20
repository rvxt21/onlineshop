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
    sizes = tree.css('ul.sku-prop-values-list li.sku-prop-value')
    if sizes and len(sizes)>0:
        sizes = [s.text(strip=True) for s in sizes]
    else:
        sizes = None
    brand_image = tree.css_first('div.brand-detail img')
    if brand_image:
        brand_image_link = f'https://tennismag.com.ua{brand_image.attributes.get("data-src")}'
    else:
        brand_image_link = None
    brand_name = characteristics.get('Бренд')
    data = {
            'Title': name,
            'Categories': categories,
            'Description': description,
            'Characteristics': characteristics,
            'Sizes': sizes,
            'Price': price,
            'Product article': product_article,
            'Old price': old_price,
            'Discount': discount,
            'Images': images,
            'Brand Image': brand_image_link,
            'Brand name': brand_name,
            'Url': url
        }
    print(data)


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

    test_collect_products_data('https://tennismag.com.ua/ua/catalog/odezhda-zhenskaya/mayka-babolat-tank-match-core/?offer=3820')


if __name__ == '__main__':
    main()