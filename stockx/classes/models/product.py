class Product:
    id = None

    def __init__(self, link, style, name, date, retail_price):
        # rename link to url.
        self.link = link
        self.style = style
        self.name = name
        self.date = date
        self.retail_price = retail_price
