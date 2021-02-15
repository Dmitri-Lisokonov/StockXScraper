from classes.context.productcontext import ProductContext
from classes.util.connectionmanager import ConnectionManager


class ProductRepository:

    def __init__(self):
        self.connection_manager = ConnectionManager()
        self.cursor = self.connection_manager.cursor
        self.context = ProductContext(self.cursor)

# CRUD Operations
    def create_product(self, product):
        self.context.create_product(product)

    def get_products(self):
        return self.context.get_products()

    def update_product(self, product, url):
        self.context.update_product(product, url)

    def delete_product(self, url):
        self.context.delete_product(url)

    def get_product_by_url(self, url):
        self.context.get_product_by_url(url)
