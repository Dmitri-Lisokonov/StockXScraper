# Logging related stuff.
import logging
logger = logging.getLogger()
fhandler = logging.FileHandler(filename='logger.log', mode='a')
formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

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
    app.scrape_sales()


if __name__ == "__main__":
    main()
