class Product:
    id = None

    def __init__(self, url, style, name, colorway, release_date, retail_price):
        # rename link to url.
        self.url = url
        self.style = style
        self.name = name
        self.colorway = colorway
        self.release_date = release_date
        self.retail_price = retail_price
