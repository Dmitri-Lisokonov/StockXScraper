from classes.context.salecontext import SaleContext
from classes.util.connectionmanager import ConnectionManager
from classes.scraper.stockx import StockxTask
from proxymanager import ProxyManager


class SaleRepository:
    def __init__(self):
        self.connection_manager = ConnectionManager()
        self.cursor = self.connection_manager.cursor
        self.context = SaleContext(self.cursor)

    # fetch sales for all products in product table
    # @param: products = list of products
    def fetch_sales_for_products(self, products):
        # Create proxy dict
        try:
            proxy_manager = ProxyManager('config/proxies.txt')
        except Exception as e:
            print(f'Could not load proxies, error: {e}')
            return

        # Scrape sales
        for product in products:
            product_class = {
                'url': product.url
            }
            stockx_task = StockxTask(product_dict=product_class, proxies=proxy_manager)
            result = stockx_task.fetch_sales_per_size()
            # Store sales in database
            for sale in result:
                print(f"Inserting {sale.url}, {sale.price}, {sale.date} into database")
                self.create_sale(sale)

    # CRUD Operations
    def create_sale(self, product):
        self.context.create_sale(product)

    def get_sales(self):
        return self.context.get_sales()

    def update_sale(self, sale):
        self.context.update_sale(sale)

    def delete_sale_by_url(self, url):
        self.context.delete_sale_by_url(url)

    def delete_sale_by_id(self, id):
        self.context.delete_sale_by_id(id)

    def get_sale_by_url(self, url):
        self.context.get_sale_by_product_url(url)

    def get_sale_by_id(self, id):
        self.context.get_sale_by_id(id)