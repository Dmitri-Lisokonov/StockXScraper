import xml.etree.ElementTree as ET
import logging

class XmlParser:
    def get_urls_by_keyword(self, sitemap, keywords):
        try:
            print('Parsing XML file URLs for keywords...')
            urls = []
            # Load all responses text and convert to XML
            for file in sitemap:
                xml_data = ET.fromstring(file)
                # Find all url tags
                for url in xml_data.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                    # Find all loc tags
                    loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    # add URLs matching to keywords
                    for keyword in keywords:
                        if keyword in loc.text:
                            urls.append(loc.text)
            # Remove duplicates
            urls = list(dict.fromkeys(urls))
            print(url)
            return urls
        except Exception as e:
            logging.error(f"Could not parse XML file => {e}")
