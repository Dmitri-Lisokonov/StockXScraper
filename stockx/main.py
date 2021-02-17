from classes.controller.applicationcontroller import AppController

# temp to test stuff
from classes.repo.productrepository import ProductRepository
from classes.repo.salerepository import SaleRepository
from classes.controller.salecontroller import SaleController
from classes.controller.productcontroller import ProductController


def main():
    # repo = ProductRepository()
    # repo.scrape_product_info()
    app = AppController()
    app.init()


if __name__ == "__main__":
    main()
