# Logging related stuff.
import logging
from classes.controller.applicationcontroller import AppController


logger = logging.getLogger()
fhandler = logging.FileHandler(filename='logger.log', mode='a')
formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():
    # repo = ProductRepository()
    # repo.scrape_product_info()
    app = AppController()
    app.scrape_products()
    # app.scrape_sales()
    # app.scrape_urls_from_sitemap()





if __name__ == "__main__":
    main()
