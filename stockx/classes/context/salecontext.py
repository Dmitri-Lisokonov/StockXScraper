from classes.models.sale import Sale


# Class for extracting and manipulating data from the product table.
# @param: cursor used from ConnectionManager class
class SaleContext:

    def __init__(self, cursor):
        self.cursor = cursor

    def create_sale(self, sale):
        query = f"INSERT INTO sale " \
                f"VALUES ('{sale.url}', '{sale.size}', '{sale.date}', '{sale.price}')"
        self.cursor.execute(query).commit()

    def get_sales(self):
        query = "SELECT * FROM sale"
        self.cursor.execute(query)
        return self.convert_to_sales_list()

    def update_sale(self, sale):
        query = f"UPDATE sale " \
                f"SET url = '{sale.url}', size = {sale.size}, date = '{sale.date}', price = '{sale.price}' " \
                f"WHERE id = {sale.id}"
        self.cursor.execute(query).commit()

    def delete_sale_by_url(self, url):
        query = f"DELETE FROM sale " \
                f"WHERE url = '{url}'"
        self.cursor.execute(query).commit()

    def delete_sale_by_id(self, id):
        query = f"DELETE FROM sale " \
                f"WHERE id = {id}"

    def get_sale_by_id(self, sale_id):
        query = f"SELECT * FROM sale " \
                f"WHERE id = {sale_id}"
        self.cursor.execute(query)
        return self.convert_to_sales_list()

    def get_sale_by_product_url(self, url):
        query = f"SELECT * FROM sale " \
                f"WHERE url = '{url}'"
        self.cursor.execute(query)
        return self.convert_to_sales_list()

        # Read all rows from result, convert to product and add to list
    def convert_to_sales_list(self):
        sale_list = []
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
            # Add converters.
            sale = Sale(row[1], row[2], row[3], row[4], row[5])
            sale.id = row[0]
            sale_list.append(sale)
        return sale_list
