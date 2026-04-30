from datetime import date

class SaleRecord:
    def __init__(self, product, quantity, sale_date, seller, region):
        self._product = product
        self._quantity = quantity
        self._date = sale_date
        self._seller = seller
        self._region = region

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, value):
        if value < 1:
            raise ValueError("Ilość musi być >= 1")
        self._quantity = value

    def get_date(self):
        return self._date

    def get_seller(self):
        return self._seller

    def get_region(self):
        return self._region

    def get_value(self):
        return self._quantity * self._product.get_price()

    def to_dict(self):
        return {
            "date": self._date.strftime("%d.%m.%Y"),
            "product_id": self._product.product_id,
            "product_name": self._product.name,
            "category": self._product.category,
            "quantity": self._quantity,
            "unit_price": self._product.get_price(),
            "value": self.get_value(),
            "seller": self._seller,
            "region": self._region
        }

    def __str__(self):
        return f"{self._date} | {self._product.name} | {self._quantity} | {self.get_value()} PLN | {self._seller} | {self._region}"