from classes.models.product import Product


# Class for extracting and manipulating data from the product table.
# @param: cursor used from ConnectionManager class
class ProductContext:
    def __init__(self, cursor):
        self.cursor = cursor

# Execute query.
    def execute(self, query):
        self.cursor.execute(query)

    def create_product(self):
        pass

    def get_products(self):
        query = "SELECT * FROM product"
        self.execute(query)
        for row in self.cursor:
            print(row)
            # Add converters.
            product = Product(row[1], row[2], row[3], row[4], row[5])
            product.id = row[0]
            product_list = [product]
        return product_list

    def update_product(self, product):
        query = f"UPDATE product " \
                f"SET stylecode = '{product.style}', name = '{product.name}', releaseDate = '{product.date}', retailPrice = {product.retail_price} " \
                f"WHERE id = {product.id}"
        print(query)
        self.execute(query)
        self.cursor.commit()

    def delete_product(self, product):
        pass

    def get_product_by_id(self, product_id):
        pass

    def get_product_by_url(self, url):
        pass
