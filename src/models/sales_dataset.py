class SalesDataset:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def filter_by_category(self, category):
        result = SalesDataset()
        for r in self.records:
            if r.get_product().category.lower() == category.lower():
                result.add_record(r)
        return result

    def filter_by_seller(self, seller):
        result = SalesDataset()
        for r in self.records:
            if r.get_seller().lower() == seller.lower():
                result.add_record(r)
        return result

    def filter_by_region(self, region):
        result = SalesDataset()
        for r in self.records:
            if r.get_region().lower() == region.lower():
                result.add_record(r)
        return result

    def filter_by_date_range(self, date_from, date_to):
        result = SalesDataset()
        for r in self.records:
            if date_from <= r.get_date() <= date_to:
                result.add_record(r)
        return result

    def get_categories(self):
        s = set()
        for r in self.records:
            s.add(r.get_product().category)
        return s

    def get_sellers(self):
        s = set()
        for r in self.records:
            s.add(r.get_seller())
        return s

    def get_regions(self):
        s = set()
        for r in self.records:
            s.add(r.get_region())
        return s

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        return iter(self.records)

    def __contains__(self, item):
        return item in self.records