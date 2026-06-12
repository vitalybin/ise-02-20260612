import json
import os
from datetime import datetime


class JsonExportService:
    def export(self, data: dict, export_typ: str, export_dir: str) -> str:
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{export_typ}_{timestamp}.json"
        filepath = os.path.join(export_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath
