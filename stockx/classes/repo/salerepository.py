from classes.context.salecontext import SaleContext
from classes.util.connectionmanager import ConnectionManager


class SaleRepository:
    def __init__(self):
        self.connection_manager = ConnectionManager()
        self.cursor = self.connection_manager.cursor
        self.context = SaleContext(self.cursor)

    # CRUD Operations
    def create_sale(self, product):
        self.context.create_sale(product)

    def get_sales(self):
        return self.context.get_sales()

    def update_sale(self, product):
        self.context.update_sale(product)

    def delete_sale_by_url(self, url):
        self.context.delete_sale_by_url(url)

    def delete_sale_by_id(self, id):
        self.context.delete_sale_by_id(id)

    def get_sale_by_url(self, url):
        self.context.get_sale_by_product_url(url)

    def get_sale_by_id(self, id):
        self.context.get_sale_by_id(id)