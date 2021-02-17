from classes.repo.salerepository import SaleRepository

class SaleController:
    def __init__(self):
        self.repo = SaleRepository()

    def fetch_sales_for_products(self, products):
        self.repo.fetch_sales_for_products(products)
