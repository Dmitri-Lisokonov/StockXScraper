import requests
import json
import time
from threading import Thread as TaskProcessor
from classes.models.product import Product
from classes.models.sale import Sale
from classes.util.proxyutil import ProxyUtil
from bs4 import BeautifulSoup
from random_useragent.random_useragent import Randomize

random_ua = Randomize()


class StockxTask(TaskProcessor):

    def __init__(self, product_dict, proxies):
        self.product_dict = product_dict
        self.proxies = proxies
        self.session = requests.session()

        self.utils = ProxyUtil()

        self.proxy = self.utils.initialize_proxy(proxies=self.proxies)
        self.session.proxies = self.proxy

        self.delay = 15
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

    def fetch_sales_per_size(self):

        sales = []

        print(f'Fetching sales for {self.product_dict["url"]}')
        try:
            response = self.session.get(self.product_dict['url'], headers=self.headers, timeout=self.timeout)
        except Exception as e:
            print(f'Could not request {self.product_dict["url"]} => {e}')
            time.sleep(self.delay)
            pass

        # Valid status code.
        if response.status_code == 200:
            # Splitting product data and loading as JSON.
            try:
                data_split = \
                response.text.split('class="product-view"><script type="application/ld+json">')[1].split("</script>")[0]
                json_response = json.loads(data_split)
                print(json_response)
            except:
                print('Could not split response / load as JSON!')
                time.sleep(self.delay)
                pass

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
                    time.sleep(self.delay)
                    continue

                # Loading response as JSON .
                json_response = json.loads(response.text)

                total = json_response["Pagination"]["total"]

                print(f'Size {size["description"]} got a total sale of: {total}')

                for i in range(total):
                    # Filter with date and add to list.
                    sale = Sale(self.product_dict["url"], json_response['ProductActivity'][i]['shoeSize'], json_response['ProductActivity'][i]['createdAt'], json_response['ProductActivity'][i]['localAmount'])
                    sales.append(sale)

        # Banned.
        elif response.status_code == 403:
            print(response.status_code)
            print(f'Could not fetch sales for {self.product_dict["url"]} - banned!')
            del self.session.cookies['__cfduid']
            # Rotate proxy here.
            time.sleep(self.delay)
            pass
        # Unknown status code.
        else:
            print(f'Could not fetch sales for {self.product_dict["url"]} - unknow status code: {response.status_code}!')
            time.sleep(self.delay)
            pass

    def fetch_product_info(self):
        try:
            response = self.session.get(self.product_dict['url'], headers=self.headers, timeout=self.timeout)
        except Exception as e:
            print(f'Could not request {self.product_dict["url"]} => {e}')
            time.sleep(self.delay)
            pass

        # Valid status code.
        if response.status_code == 200:
            try:
                # Parse product information.
                # Parse product information.
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
                product = Product(self.product_dict["url"], style_code, name, colorway, date, retail_price)
                print(f'fetched info for product, style: {style_code} cw: {colorway} retail price: {retail_price} date: {date}')
            except:
                print('Could not split response / load as JSON!')
                time.sleep(self.delay)
                pass
            # Banned.
        elif response.status_code == 403:
            print(response.status_code)
            print(f'Could not fetch sales for {self.product_dict["url"]} - banned!')
            del self.session.cookies['__cfduid']
            # Rotate proxy here.
            time.sleep(self.delay)
            pass
            # Unknown status code.
        else:
            print(f'Could not fetch product info for {self.product["url"]} - unknow status code: {response.status_code}!')
            time.sleep(self.delay)
            pass
        return product