from classes.entity.product import Product


# Class for extracting and manipulating data from the product table.
# @param: cursor used from ConnectionManager class
class ProductContext:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_product(self, product):
        query = f"INSERT INTO product " \
                f"VALUES ('{product.url}', '{product.style}', '{product.name}', '{product.colorway}' '{product.release_date}', {product.retail_price})"
        self.cursor.execute(query).commit()

    def get_products(self):
        query = "SELECT * FROM product"
        self.cursor.execute(query)
        return self.convert_to_product_list()

    def get_products_without_info(self):
        query = "SELECT * FROM product " \
                "WHERE styleCode IS NULL AND name IS NULL AND colorway IS NULL AND releaseDate IS NULL AND retailPrice IS NULL"
        self.cursor.execute(query)
        return self.convert_to_product_list()

    def update_product(self, product, url):
        query = f"UPDATE product " \
                f"SET url = '{product.url}', stylecode = '{product.style}', name = '{product.name}', colorway = '{product.colorway}', releaseDate = '{product.release_date}', retailPrice = {product.retail_price} " \
                f"WHERE url = '{url}'"
        self.cursor.execute(query).commit()

    def delete_product(self, url):
        query = f"DELETE FROM product " \
                f"WHERE url = '{url}'"
        self.cursor.execute(query).commit()

    def get_product_by_url(self, url):
        query = f"SELECT * FROM product " \
                f"WHERE url = '{url}'"
        self.cursor.execute(query)
        return self.convert_to_product_list()

    # Read all rows from result, convert to product and add to list
    def convert_to_product_list(self):
        product_list = []
        rows = self.cursor.fetchall()
        for row in rows:
            product = Product(row[0], row[1], row[2], row[3], row[4], row[5])
            product_list.append(product)
        return product_list
