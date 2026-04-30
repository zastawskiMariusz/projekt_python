class SalesStatistics:
    def __init__(self, dataset):
        self.dataset = dataset

    def total_revenue(self):
        total = 0
        for r in self.dataset:
            total += r.get_value()
        return total

    def average_transaction(self):
        if len(self.dataset) == 0:
            raise ValueError("Brak danych")
        return self.total_revenue() / len(self.dataset)

    def revenue_by_category(self):
        result = {}
        for r in self.dataset:
            cat = r.get_product().category
            result[cat] = result.get(cat, 0) + r.get_value()
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def revenue_by_seller(self):
        result = {}
        for r in self.dataset:
            seller = r.get_seller()
            result[seller] = result.get(seller, 0) + r.get_value()
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def revenue_by_region(self):
        result = {}
        for r in self.dataset:
            region = r.get_region()
            result[region] = result.get(region, 0) + r.get_value()
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def monthly_summary(self):
        result = {}
        for r in self.dataset:
            key = r.get_date().strftime("%Y-%m")
            result[key] = result.get(key, 0) + r.get_value()
        return dict(sorted(result.items()))

    def top_products(self, n=5):
        result = {}
        for r in self.dataset:
            pid = r.get_product().product_id
            name = r.get_product().name
            key = f"{pid} {name}"
            result[key] = result.get(key, 0) + r.get_value()

        sorted_items = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:n]

    def best_seller(self):
        data = self.revenue_by_seller()
        if not data:
            return None
        return list(data.items())[0]

    def best_month(self):
        data = self.monthly_summary()
        if not data:
            return None
        return sorted(data.items(), key=lambda x: x[1], reverse=True)[0]