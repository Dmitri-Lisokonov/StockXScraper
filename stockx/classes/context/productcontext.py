import logging
from classes.entity.product import Product


# Class for extracting and manipulating data from the product table.
# @param: cursor used from ConnectionManager class
class ProductContext:
    def __init__(self, cursor):
        self.cursor = cursor

    def bulk_insert_url(self, url_list):
        self.cursor.fast_executemany = True
        query = f"INSERT INTO product (url) VALUES (?)"
        self.cursor.executemany(query, url_list)
        self.cursor.commit()

    def bulk_create_product(self, product_list):
        self.cursor.fast_executemany = True
        query = f"INSERT INTO product (url, styleCode, name, colorway, releaseDate, retailPrice) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(query, product_list)
        self.cursor.commit()

    def create_product(self, product):
        if product.style is None and product.name is None and product.colorway is None and product.release_date is None and product.retail_price is None:
            print(f'adding: {product.url}')
            query = f"INSERT INTO product (url)" \
                    f"VALUES ('{product.url}')"
        else:
            query = f"INSERT INTO product " \
                    f"VALUES ('{product.url}', '{product.style}', '{product.name}', '{product.colorway}' '{product.release_date}', {product.retail_price})"
        try:
            self.cursor.execute(query).commit()
        except Exception as e:
            logging.error(f"Could not create product => {e}")
            raise e

    def get_products(self):
        query = "SELECT * FROM product"
        try:
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Could not get products => {e}")
            raise e
        return self.convert_to_product_list()

    def get_products_without_info(self):
        query = "SELECT * FROM product " \
                "WHERE styleCode IS NULL AND name IS NULL AND colorway IS NULL AND releaseDate IS NULL AND retailPrice IS NULL"
        try:
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Could not get products without info => {e}")
            raise e
        return self.convert_to_product_list()

    def update_product(self, product, url):
        query = f"UPDATE product " \
                f"SET url = '{product.url}', stylecode = '{product.style}', name = '{product.name}', colorway = '{product.colorway}', releaseDate = '{product.release_date}', retailPrice = {product.retail_price} " \
                f"WHERE url = '{url}'"
        try:
            self.cursor.execute(query).commit()
        except Exception as e:
            logging.error(f"Could not update product: {product} {url} => {e}")
            raise e

    def delete_product(self, url):
        query = f"DELETE FROM product " \
                f"WHERE url = '{url}'"
        try:
            self.cursor.execute(query).commit()
        except Exception as e:
            logging.error(f"Could not delete product: {url} => {e}")
            raise e

    def get_product_by_url(self, url):
        query = f"SELECT * FROM product " \
                f"WHERE url = '{url}'"
        try:
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Could not get product by url: {url} => {e}")
            raise e
        return self.convert_to_product_list()

    # Read all rows from result, convert to product and add to list
    def convert_to_product_list(self):
        product_list = []
        rows = self.cursor.fetchall()
        try:
            for row in rows:
                product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
                product_list.append(product)
        except Exception as e:
            logging.error(f"Could not convert to product list => {e}")
            raise e
        return product_list
