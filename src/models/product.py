class Product:
    def __init__(self, product_id, name, category, price):
        self.product_id = product_id
        self.name = name
        self.category = category
        self._price = price

    def get_price(self):
        return self._price

    def set_price(self, value):
        if value <= 0:
            raise ValueError(f"Nieprawidłowa cena: {value}")
        self._price = value

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Nieprawidłowy procent rabatu")
        return self._price * (1 - percent / 100)

    def __str__(self):
        return f"[{self.product_id}] {self.name} ({self.category}) - {self._price} PLN"

    def __eq__(self, other):
        return self.product_id == other.product_id