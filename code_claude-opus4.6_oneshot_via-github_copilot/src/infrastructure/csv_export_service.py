import csv
import os
from datetime import datetime


class CsvExportService:
    def export(self, data: dict, export_typ: str, export_dir: str) -> str:
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{export_typ}_{timestamp}.csv"
        filepath = os.path.join(export_dir, filename)

        rows = []
        for key, items in data.items():
            if isinstance(items, list) and len(items) > 0:
                rows = items
                break

        if not rows:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("")
            return filepath

        fieldnames = list(rows[0].keys())
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for row in rows:
                writer.writerow({k: str(v) for k, v in row.items()})

        return filepath
