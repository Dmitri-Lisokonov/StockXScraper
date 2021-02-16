from classes.repo.productrepository import ProductRepository
from classes.scraper.stockx import StockxTask

def main():
    repo = ProductRepository()
    repo.scrape_product_info()



if __name__ == "__main__":
    main()
