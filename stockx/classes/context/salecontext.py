import logging
from classes.entity.sale import Sale


# Class for extracting and manipulating data from the product table.
# @param: cursor used from ConnectionManager class
class SaleContext:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_sale(self, sale):
        query = f"INSERT INTO sale " \
                f"VALUES ('{sale.url}', '{sale.size}', '{sale.date}', '{sale.price}')"
        try:
            self.cursor.execute(query).commit()
        except Exception as e:
            logging.error(f"Could not create sale: {sale} => {e}")
            raise e

    def get_sales(self):
        query = "SELECT * FROM sale"
        try:
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Could not get sales => {e}")
            raise e
        return self.convert_to_sales_list()

    def update_sale(self, sale):
        query = f"UPDATE sale " \
                f"SET url = '{sale.url}', size = {sale.size}, date = '{sale.date}', price = '{sale.price}' " \
                f"WHERE id = {sale.id}"
        try:
            self.cursor.execute(query).commit()
        except Exception as e:
            logging.error(f"Could not update sale: {sale} => {e}")
            raise e

    def delete_sale_by_url(self, url):
        query = f"DELETE FROM sale " \
                f"WHERE url = '{url}'"
        try:
            self.cursor.execute(query).commit()
        except Exception as e:
            logging.error(f"Could not delete sale by url: {url} => {e}")
            raise e 

    def delete_sale_by_id(self, id):
        query = f"DELETE FROM sale " \
                f"WHERE id = {id}"

        
        try:
            self.cursor.execute(query).commit()
        except Exception as e:
            logging.error(f"Could not delete sale by id: {id} => {e}")
            raise e

    def get_sale_by_id(self, sale_id):
        query = f"SELECT * FROM sale " \
                f"WHERE id = {sale_id}"

        try:
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Could not get sale by id: {sale_id} => {e}")
            raise e
        return self.convert_to_sales_list()

    def get_sale_by_product_url(self, url):
        query = f"SELECT * FROM sale " \
                f"WHERE url = '{url}'"

        try:
            self.cursor.execute(query)
        except Exception as e:
            logging.error(f"Could not get sale by product url: {url} => {e}")
            raise e
        return self.convert_to_sales_list()

        # Read all rows from result, convert to product and add to list
    def convert_to_sales_list(self):
        sale_list = []
        rows = self.cursor.fetchall()
        try:
            for row in rows:
                sale = Sale(row[1], row[2], row[3], row[4])
                sale.id = row[0]
                sale_list.append(sale)
        except Exception as e:
            logging.error(f"Could not conver to sales list => {e}")
            raise e
        return sale_list
