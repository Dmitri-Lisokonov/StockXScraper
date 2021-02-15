from classes.util.connectionmanager import ConnectionManager
from classes.context.productcontext import ProductContext
from classes.models.product import Product

conn_manager = ConnectionManager()
product_manager = ProductContext(conn_manager.cursor)

def main():
    # thread_list = []
    #
    # try:
    #     proxy_manager = ProxyManager('config/proxies.txt')
    # except Exception as e:
    #     print(f'Could not load proxies, error: {e}')
    #     return
    # # Fetch URLS and append to list.
    #
    # # Start thread per URL that scrapes every 10 PM.
    #
    # # Returns a list with dictionaries that contains product data.
    # products = ['https://stockx.com/air-jordan-5-retro-what-the']
    #
    # # Loop trough products.
    # for product in products:
    #     # Initialize product.
    #     # product_class = Product(product)
    #     product_class = {
    #         'url': product
    #     }
    #
    #     stockx_task = StockxTask(product=product_class, proxies=proxy_manager)
    #     stockx_thread = threading.Thread(target=stockx_task.fetch_sales_per_size(), args=())
    #     thread_list.append(stockx_thread)
    #
    # # Looping trough all tasks and starting them.
    # for thread in thread_list:
    #     thread.start()

    new_product = Product(link='www.product.com', style='new_style1', name='Patta', retail_price='1337', date='11-02-2004')
    new_product.id = 1
    product_manager.update_product(new_product)
    products = product_manager.get_products()
    print(products[0].id, products[0].link, products[0].retail_price, products[0].date, products[0].style)


if __name__ == "__main__":
    main()
