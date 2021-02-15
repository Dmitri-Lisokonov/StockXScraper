import requests
import time


class ProxyUtil:
    # Rotate proxy.
    def rotate_session(self, session, proxies):
        random_proxy = proxies.random_proxy().get_dict()
        old_session_cookies = session.cookies
        # New session.
        new_session = requests.Session()
        # Adding old session cookies to new session.
        new_session.cookies = old_session_cookies
        # Adding proxy.
        new_session.proxies = random_proxy
        # Deleting everything related to old session.
        session.close()
        del session
        return new_session

    # Initialize proxy function.
    @staticmethod
    def initialize_proxy(proxies):
        random_proxy = proxies.random_proxy().get_dict()
        print(random_proxy)
        time.sleep(1)
        return random_proxy
