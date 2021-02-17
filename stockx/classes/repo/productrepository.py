from classes.context.productcontext import ProductContext
from classes.util.connectionmanager import ConnectionManager
from classes.scraper.stockx import StockxTask
from proxymanager import ProxyManager


class ProductRepository:
    def __init__(self):
        self.connection_manager = ConnectionManager()
        self.cursor = self.connection_manager.cursor
        self.context = ProductContext(self.cursor)

    def scrape_product_info(self):
        # Create proxy dict
        try:
            proxy_manager = ProxyManager('config/proxies.txt')
        except Exception as e:
            print(f'Could not load proxies, error: {e}')
            return
        # Get products with NULL values(empty)
        products = self.get_products_without_info()

        # Scrape product information
        for product in products:
            product_dict = {
                'url': product.url
            }
            stockx_task = StockxTask(product_dict=product_dict, proxies=proxy_manager)
            result = stockx_task.fetch_product_info()
            # Store info in database
            self.update_product(result, product.url)

    # CRUD Operations
    def create_product(self, product):
        self.context.create_product(product)

    def get_products(self):
        return self.context.get_products()

    def get_products_without_info(self):
        return self.context.get_products_without_info()

    def update_product(self, product, url):
        self.context.update_product(product, url)

    def delete_product(self, url):
        self.context.delete_product(url)

    def get_product_by_url(self, url):
        self.context.get_product_by_url(url)
