from classes.context.productcontext import ProductContext
from classes.util.connectionmanager import ConnectionManager
from classes.entity.product import Product
from classes.util.xmlparser import XmlParser
from classes.scraper.xmlscraper import XmlScraper
from classes.scraper.stockx import StockxTask
from classes.util.stringparser import StringParser
from proxymanager import ProxyManager


class ProductRepository:
    def __init__(self):
        self.connection_manager = ConnectionManager()
        self.cursor = self.connection_manager.cursor
        self.context = ProductContext(self.cursor)
        self.xml_parser = XmlParser()
        self.string_parser = StringParser()

    def scrape_product_info(self):
        # Create proxy dict
        result_list = []
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
            paramlist = [result]
            result_list.append(paramlist)
        self.bulk_create_product(result_list)


        # # Scrape product information
        # for product in products:
        #     product_dict = {
        #         'url': product.url
        #     }
        #     stockx_task = StockxTask(product_dict=product_dict, proxies=proxy_manager)
        #     result = stockx_task.fetch_product_info()
        #     # Store info in database
        #     self.update_product(result, product.url)

    def scrape_urls_from_sitemap(self):
        xml_list = ['https://stockx.com/de-de/sitemap/sitemap-0.xml',
                    'https://stockx.com/de-de/sitemap/sitemap-1.xml',
                    'https://stockx.com/de-de/sitemap/sitemap-2.xml']

        xml_scraper = XmlScraper(xml_list)
        sitemap = xml_scraper.scrape_site_map()
        keywords = self.string_parser.parse_keywords('config/keywords.txt')
        urls = self.xml_parser.get_urls_by_keyword(sitemap, keywords)
        self.bulk_insert_url(urls)

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
        return self.context.get_product_by_url(url)

    def bulk_create_product(self, product_list):
        self.context.bulk_create_product(product_list)

    def bulk_insert_url(self, url_list):
        self.context.bulk_insert_url(url_list)
