from classes.controller.salecontroller import SaleController
from classes.controller.productcontroller import ProductController


class AppController:

    def __init__(self):
        self.sale_controller = SaleController()
        self.product_controller = ProductController()

    def scrape_urls(self):
        # To be implemented
        pass

    def scrape_products(self):
        self.product_controller.scrape_product_info()

    def scrape_sales(self):
        products = self.product_controller.get_all_products()
        self.sale_controller.fetch_sales_for_products(products)

    def init(self):
        print('Please select an option:')
        print('1. Scrape for URLs')
        print('2. Scrape product information')
        print('3. Scrape sales for all products')
        user_input = int(input())
        if user_input == 1:
            self.scrape_urls()
        elif user_input == 2:
            self.scrape_products()
        elif user_input == 3:
            self.scrape_sales()
        else:
            print('Invalid user input. Please type 1, 2 or 3 and press ENTER.')