import os
import json
from datetime import datetime
from src.models.product import Product
from src.models.sale_record import SaleRecord
from src.models.sales_dataset import SalesDataset


class SdfParseError(Exception):
    pass


class FileProcessor:

    ALLOWED_REGIONS = ["WA", "KR", "GD", "PO", "WR", "LO", "RZ", "BY", "ZG", "OP"]

    def parse_sdf(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("Brak pliku")

        dataset = SalesDataset()
        errors = []
        products = {}

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        section = None
        section_order = []

        for i, line in enumerate(lines, start=1):
            line = line.strip()

            if line == "" or line.startswith("#") or line == "---":
                if line in ["#DATASET", "#PRODUCTS", "#TRANSACTIONS"]:
                    section = line
                    section_order.append(line)
                continue

            if section is None:
                raise SdfParseError("Brak sekcji")

            # ------------------ PRODUCTS ------------------
            if section == "#PRODUCTS":
                parts = line.split("|")
                if len(parts) != 4:
                    raise SdfParseError(f"Linia {i}: błędny produkt")

                pid, name, cat, price = parts

                try:
                    price = float(price)
                except:
                    raise SdfParseError(f"Linia {i}: zła cena")

                products[pid] = Product(pid, name, cat, price)

            # ------------------ TRANSACTIONS ------------------
            elif section == "#TRANSACTIONS":
                parts = line.split("|")

                if len(parts) != 5:
                    errors.append(f"Linia {i}: zła liczba pól")
                    continue

                date_str, pid, qty, seller, region = parts

                # sprawdzenie produktu
                if pid not in products:
                    errors.append(f"Linia {i}: nieznany produkt")
                    continue

                # data
                try:
                    date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
                except:
                    errors.append(f"Linia {i}: zła data")
                    continue

                # ilość
                try:
                    qty = int(qty)
                    if qty < 1:
                        raise ValueError()
                except:
                    errors.append(f"Linia {i}: zła ilość")
                    continue

                # region
                if region not in self.ALLOWED_REGIONS:
                    errors.append(f"Linia {i}: zły region")
                    continue

                record = SaleRecord(
                    products[pid],
                    qty,
                    date_obj,
                    seller,
                    region
                )

                dataset.add_record(record)

        # sprawdzenie sekcji
        if section_order != ["#DATASET", "#PRODUCTS", "#TRANSACTIONS"]:
            raise SdfParseError("Zła kolejność sekcji")

        return dataset, errors

    def save_report(self, path, text):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        except PermissionError:
            raise PermissionError("Brak uprawnień zapisu")

    def save_json(self, path, data):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except PermissionError:
            raise PermissionError("Brak uprawnień zapisu")