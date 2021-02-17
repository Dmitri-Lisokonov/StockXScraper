from classes.repo.productrepository import ProductRepository


class ProductController:
    def __init__(self):
        self.repo = ProductRepository()

    def scrape_product_info(self):
        self.repo.scrape_product_info()

    def get_all_products(self):
        return self.repo.get_products()
