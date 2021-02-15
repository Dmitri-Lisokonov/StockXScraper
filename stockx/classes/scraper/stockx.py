import requests
import json
import time
from threading import Thread as TaskProcessor
from classes.models.product import Product
# Random useragent.
from random_useragent.random_useragent import Randomize

random_ua = Randomize()

from classes.util.proxyutil import ProxyUtil


class Task(TaskProcessor):
    def __init__(self, product, proxies):
        self.product = product
        self.proxies = proxies
        self.session = requests.session()

        self.utils = Utils()

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

        products = []

        print(f'Fetching sales for {self.product["url"]}')
        try:
            response = self.session.get(self.product['url'], headers=self.headers, timeout=self.timeout)
        except Exception as e:
            print(f'Could not request {self.product["url"]} => {e}')
            time.sleep(self.delay)
            pass

        # Valid status code.
        if response.status_code == 200:
            # Splitting product data and loading as JSON.
            try:
                data_split = \
                response.text.split('class="product-view"><script type="application/ld+json">')[1].split("</script>")[0]
                json_response = json.loads(data_split)
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
                    product = Product(json_response['ProductActivity'][i]['shoeSize'], json_response['ProductActivity'][i]['localAmount'], json_response['ProductActivity'][i]['createdAt'])
                    products.append(product)
                    print(f"size:{products[i].size}, price: {products[i].price}, date: {products[i].date}")
        # Banned.
        elif response.status_code == 403:
            print(response.status_code)
            print(f'Could not fetch sales for {self.product["url"]} - banned!')
            del self.session.cookies['__cfduid']
            # Rotate proxy here.
            time.sleep(self.delay)
            pass
        # Unknown status code.
        else:
            print(f'Could not fetch sales for {self.product["url"]} - unknow status code: {response.status_code}!')
            time.sleep(self.delay)
            pass
