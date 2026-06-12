import json
import os
from domain.repositories import IImportValidator
from domain.enums import GeraeteTyp, GeraeteStatus, Rolle


class ImportService(IImportValidator):
    def __init__(self, import_dir: str = "/app/imports"):
        self.import_dir = import_dir

    def validate(self, importData) -> list:
        fehler = []
        valid_types = {t.value for t in GeraeteTyp}
        valid_status = {s.value for s in GeraeteStatus}
        valid_rollen = {r.value for r in Rolle}

        if "geraete" in importData:
            seen_ids = set()
            for i, g in enumerate(importData["geraete"]):
                if not g.get("name"):
                    fehler.append(f"Geraet {i}: Pflichtfeld 'name' fehlt")
                if g.get("typ") not in valid_types:
                    fehler.append(f"Geraet {i}: Ungueltiger Typ '{g.get('typ')}'")
                if g.get("status") not in valid_status:
                    fehler.append(f"Geraet {i}: Ungueltiger Status '{g.get('status')}'")
                if g.get("status") == "INSTALLIERT" and not g.get("raumId"):
                    fehler.append(f"Geraet {i}: Installiert ohne Raumzuordnung")
                gid = g.get("geraetId")
                if gid is not None:
                    if gid in seen_ids:
                        fehler.append(f"Geraet {i}: Doppelte ID {gid}")
                    seen_ids.add(gid)

        if "users" in importData:
            for i, u in enumerate(importData["users"]):
                if not u.get("username"):
                    fehler.append(f"User {i}: Pflichtfeld 'username' fehlt")
                if u.get("rolle") not in valid_rollen:
                    fehler.append(f"User {i}: Ungueltige Rolle '{u.get('rolle')}'")

        return fehler

    def list_files(self):
        os.makedirs(self.import_dir, exist_ok=True)
        return [
            f for f in os.listdir(self.import_dir)
            if f.endswith((".json", ".csv"))
        ]
