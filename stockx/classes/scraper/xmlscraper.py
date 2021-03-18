import requests
import logging


# Consider adding this to stockx class.
class XmlScraper:
    def __init__(self, url_list):
        self.urls = url_list

    def scrape_site_map(self):
        xml_session = requests.session()
        xml_responses = []
        for url in self.urls:
            try:
                print('Fetching sitemap...')
                response = xml_session.get(url)
                xml_responses.append(response.text)
            except Exception as e:
                logging.error(f"Could not request sitemap: {url}")
        if xml_responses is not None:
            return xml_responses
