import os
from datetime import datetime
from src.io.file_processor import FileProcessor, SdfParseError
from src.analysis.statistics import SalesStatistics


class ConsoleApp:
    def __init__(self, reports_dir):
        self.reports_dir = reports_dir
        self.dataset = None
        self.errors = []
        self.processor = FileProcessor()
        self.index = "unknown"

    def run(self):
        while True:
            print("\n===== MENU =====")
            print("1. Wczytaj plik SDF")
            print("2. Statystyki ogólne")
            print("3. Filtruj i przeglądaj")
            print("4. Raport tekstowy")
            print("5. Eksport JSON")
            print("6. Informacje o zbiorze")
            print("0. Wyjście")

            choice = input("Wybierz opcję: ")

            try:
                if choice == "1":
                    self.load_file()
                elif choice == "2":
                    self.show_stats()
                elif choice == "3":
                    self.filter_menu()
                elif choice == "4":
                    self.save_report()
                elif choice == "5":
                    self.export_json()
                elif choice == "6":
                    self.show_info()
                elif choice == "0":
                    break
                else:
                    print("Nieznana opcja")
            except Exception as e:
                print("Błąd:", e)

    def load_file(self):
        path = input("Podaj ścieżkę do pliku: ")

        try:
            self.dataset, self.errors = self.processor.parse_sdf(path)
            self.index = os.path.basename(path).split(".")[0]

            print("Wczytano:", len(self.dataset))
            print("Błędów:", len(self.errors))

            if len(self.errors) > 0:
                print("\nBłędy:")
                for e in self.errors[:10]:
                    print(e)
                if len(self.errors) > 10:
                    print(f"... i {len(self.errors)-10} więcej")

        except SdfParseError as e:
            print("Błąd krytyczny:", e)

    def show_stats(self):
        if not self.dataset:
            print("Najpierw wczytaj dane")
            return

        stats = SalesStatistics(self.dataset)

        print("\nŁączny przychód:", round(stats.total_revenue(), 2))
        print("Liczba transakcji:", len(self.dataset))
        print("Średnia:", round(stats.average_transaction(), 2))

        print("\nNajlepszy sprzedawca:", stats.best_seller())
        print("Najlepszy miesiąc:", stats.best_month())

        print("\nPrzychód wg kategorii:")
        for k, v in stats.revenue_by_category().items():
            print(k, ":", round(v, 2))

        print("\nPrzychód wg regionu:")
        for k, v in stats.revenue_by_region().items():
            print(k, ":", round(v, 2))

        print("\nTop produkty:")
        for p in stats.top_products():
            print(p)

    def filter_menu(self):
        if not self.dataset:
            print("Najpierw wczytaj dane")
            return

        print("\n1. Kategoria")
        print("2. Sprzedawca")
        print("3. Zakres dat")
        print("4. Region")

        choice = input("Wybierz: ")

        filtered = None

        if choice == "1":
            val = input("Podaj kategorię: ")
            filtered = self.dataset.filter_by_category(val)

        elif choice == "2":
            val = input("Podaj sprzedawcę: ")
            filtered = self.dataset.filter_by_seller(val)

        elif choice == "3":
            d1 = input("Od (DD.MM.RRRR): ")
            d2 = input("Do (DD.MM.RRRR): ")
            d1 = datetime.strptime(d1, "%d.%m.%Y").date()
            d2 = datetime.strptime(d2, "%d.%m.%Y").date()
            filtered = self.dataset.filter_by_date_range(d1, d2)

        elif choice == "4":
            val = input("Podaj region: ")
            filtered = self.dataset.filter_by_region(val)

        else:
            print("Zła opcja")
            return

        print("\n--- WYNIKI ---")
        for r in filtered:
            print(r)

        stats = SalesStatistics(filtered)
        print("\nSuma:", round(stats.total_revenue(), 2))

    def save_report(self):
        if not self.dataset:
            print("Najpierw wczytaj dane")
            return

        stats = SalesStatistics(self.dataset)

        text = "RAPORT\n"
        text += f"Transakcji: {len(self.dataset)}\n"
        text += f"Przychód: {stats.total_revenue()}\n\n"

        for k, v in stats.monthly_summary().items():
            text += f"{k}: {v}\n"

        name = f"{self.index}_raport_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt"
        path = os.path.join(self.reports_dir, name)

        self.processor.save_report(path, text)
        print("Zapisano:", path)

    def export_json(self):
        if not self.dataset:
            print("Najpierw wczytaj dane")
            return

        data = []

        for r in self.dataset:
            data.append(r.to_dict())

        name = f"{self.index}_export_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
        path = os.path.join(self.reports_dir, name)

        self.processor.save_json(path, data)
        print("Zapisano:", path)

    def show_info(self):
        if not self.dataset:
            print("Najpierw wczytaj dane")
            return

        print("Rekordów:", len(self.dataset))
        print("Kategorie:", self.dataset.get_categories())
        print("Sprzedawcy:", self.dataset.get_sellers())
        print("Regiony:", self.dataset.get_regions())