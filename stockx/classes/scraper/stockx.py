import logging
import requests
import json
import time
from threading import Thread as TaskProcessor
from classes.entity.product import Product
from classes.entity.sale import Sale
from classes.util.proxyutil import ProxyUtil
from bs4 import BeautifulSoup
from random_useragent.random_useragent import Randomize

# MOVE THIS
random_ua = Randomize()


class StockxTask(TaskProcessor):

    def __init__(self, product_dict, proxies):
        self.product_dict = product_dict
        self.proxies = proxies
        self.session = requests.session()

        self.utils = ProxyUtil()

        self.proxy = self.utils.initialize_proxy(proxies=self.proxies)
        self.session.proxies = self.proxy

        self.delay = 0.5
        self.timeout = 60
        self.user_agent = random_ua.random_agent('desktop', 'windows')
        self.headers = {
            'authority': 'stockx.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    # Fetch sales
    def fetch_sales_per_size(self):

        sales = []
        while True:
            print(f'Fetching sales for {self.product_dict["url"]}')
            try:
                response = self.session.get(self.product_dict['url'], headers=self.headers, timeout=self.timeout)
            except Exception as e:
                print(f'Could not request {self.product_dict["url"]} => {e}')
                logging.error(f"Could not request {self.product_dict['url']} (fetch sales per size) => {e}")
                time.sleep(self.delay)
                continue

            # Valid status code.
            if response.status_code == 200:
                # Splitting product data and loading as JSON.
                try:
                    data_split = \
                        response.text.split('class="product-view"><script type="application/ld+json">')[1].split(
                            "</script>")[0]
                    json_response = json.loads(data_split)
                except:
                    print('Could not split response / load as JSON!')
                    logging.error(f"Could not split response / load as json (fetch sales per size) => {e}")
                    time.sleep(self.delay)
                    continue

                # Looping trough sizes.
                for size in json_response['offers']['offers']:
                    params = (
                        ('state', '480'),
                        ('currency', 'EUR'),
                        ('limit', '250'),
                        ('page', '1'),
                        ('sort', 'createdAt'),
                        ('order', 'DESC'),
                        ('country', 'NL'),
                    )

                    print(f'Requesting sales for size {size["description"]} {size["sku"]}')

                    try:
                        response = self.session.get(f'https://stockx.com/api/products/{size["sku"]}/activity',
                                                    headers=self.headers, params=params, timeout=self.timeout)
                    except:
                        print(f'Could not request sales for size {size["description"]}!')
                        logging.error(
                            f"Could not request sales for size {size['description']} (fetch sales per size) => {e}")
                        time.sleep(self.delay)
                        continue

                    # Loading response as JSON .
                    json_response = json.loads(response.text)

                    try:
                        total = json_response["Pagination"]["total"]
                    except Exception as e:
                        print(f'Could not fetch total => {e}!')
                        logging.error(f"Could not fetch total => {e}!")
                        time.sleep(self.delay)
                        continue

                    print(f'Size {size["description"]} got a total sale of: {total}')

                    for i in range(total):
                        # Filter with date and add to list.
                        sale = Sale(self.product_dict["url"], json_response['ProductActivity'][i]['shoeSize'],
                                    json_response['ProductActivity'][i]['createdAt'],
                                    json_response['ProductActivity'][i]['localAmount'])
                        sales.append(sale)
                break
            # Banned.
            elif response.status_code == 403:
                print(f'Could not fetch sales for {self.product_dict["url"]} - banned!')
                del self.session.cookies['__cfduid']
                logging.critical(f"Could not fetch sales for {self.product_dict['url']} - status code Banned!")
                # Rotate proxy here.
                time.sleep(self.delay)
                continue
            # Unknown status code.
            else:
                print(
                    f'Could not fetch sales for {self.product_dict["url"]} - unknow status code: {response.status_code}!')
                logging.critical(
                    f"Could not fetch sales for {self.product_dict['url']} - status code {response.status_code}!")
                time.sleep(self.delay)
                continue

        return sales

    # Fetch product information.
    def fetch_product_info(self):

        while True:
            try:
                response = self.session.get(self.product_dict['url'], headers=self.headers, timeout=self.timeout)
            except Exception as e:
                print(f'Could not request {self.product_dict["url"]} => {e}')
                logging.error(f"Could not request product information (fetch_product_info) => {e}")
                continue

            # Valid status code.
            if response.status_code == 200:
                try:
                    # Parse product information.
                    # Below info maybe found in JSON?
                    response.text
                    soup = BeautifulSoup(response.text, 'html.parser')
                    element = soup.find('span', {'data-testid': 'product-detail-style'})
                    style_code = element.text.strip()
                    element = soup.find('span', {'data-testid': 'product-detail-colorway'})
                    colorway = element.text.strip()
                    element = soup.find('span', {'data-testid': 'product-detail-retail price'})
                    retail_price = element.text.strip()
                    element = soup.find('span', {'data-testid': 'product-detail-release date'})
                    date = element.text.strip()
                    element = soup.find('h1', {'data-testid': 'product-name'})
                    name = element.text.strip()
                    product = Product(self.product_dict["url"], "style", name, colorway, date, retail_price)
                    print(
                        f'fetched info for product, style: "style" cw: {colorway} retail price: {retail_price} date: {date}')
                except Exception as e:
                    print('Could not split response / load as JSON!')
                    logging.critical(f"Could not split response / load as JSON (fetch product info) => {e}")
                    continue
                break
                # Banned.
            elif response.status_code == 403:
                print(f'Could not fetch sales for {self.product_dict[""]} - banned!')
                logging.critical(f"Could not fetch sales for {self.product_dict['url']} - status code Banned!")
                del self.session.cookies['__cfduid']
                # Rotate proxy here.
                time.sleep(self.delay)
                continue
            # Unknown status code.
            else:
                print(
                    f'Could not fetch product info for {self.product["url"]} - unknow status code: {response.status_code}!')
                logging.critical(
                    f"Could not fetch sales for {self.product_dict['url']} - status code {response.status_code}!")
                time.sleep(self.delay)
                continue
        time.sleep(self.delay)
        return product
