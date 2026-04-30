from src.app.console_app import ConsoleApp

if __name__ == "__main__":
    app = ConsoleApp(reports_dir="data/reports")
    app.run()