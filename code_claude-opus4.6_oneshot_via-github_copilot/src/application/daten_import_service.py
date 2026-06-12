import json
import os
from domain.repositories import IRaumRepository, IGeraetRepository, IBackupRepository
from domain.backup_auftrag import BackupAuftrag
from domain.enums import Berechtigung, GeraeteTyp, GeraeteStatus
from domain.smart_geraet_factory import SmartGeraetFactory
from domain.raum import Raum
from application.berechtigungs_service import BerechtigungsService


class DatenImportService:
    def __init__(self, raum_repo: IRaumRepository, geraet_repo: IGeraetRepository,
                 backup_repo: IBackupRepository,
                 berechtigungs_service: BerechtigungsService,
                 import_dir: str = "/app/imports"):
        self.raum_repo = raum_repo
        self.geraet_repo = geraet_repo
        self.backup_repo = backup_repo
        self.berechtigungs_service = berechtigungs_service
        self.import_dir = import_dir

    def execute(self, user, filename: str) -> dict:
        self.berechtigungs_service.execute(user, Berechtigung.DATEN_BACKUP_EXPORT_IMPORT)
        filepath = os.path.join(self.import_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Importdatei nicht gefunden: {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            import_data = json.load(f)

        protokoll = {"fehler": [], "importiert_raeume": 0, "importiert_geraete": 0}
        self._validate(import_data, protokoll)

        if protokoll["fehler"]:
            auftrag = BackupAuftrag(
                jobType="import", filePath=filepath,
                createdBy=user.username, status="fehlgeschlagen"
            )
            self.backup_repo.saveJob(auftrag)
            return protokoll

        if "raeume" in import_data:
            for rd in import_data["raeume"]:
                raum = Raum(name=rd["name"], beschreibung=rd.get("beschreibung", ""))
                self.raum_repo.save(raum)
                protokoll["importiert_raeume"] += 1

        if "geraete" in import_data:
            for gd in import_data["geraete"]:
                typ = GeraeteTyp(gd["typ"])
                geraet = SmartGeraetFactory.create(typ, gd["name"])
                geraet.status = GeraeteStatus(gd["status"])
                geraet.raumId = gd.get("raumId")
                geraet.configuration = gd.get("configuration", {})
                self.geraet_repo.save(geraet)
                protokoll["importiert_geraete"] += 1

        auftrag = BackupAuftrag(
            jobType="import", filePath=filepath,
            createdBy=user.username, status="erfolgreich"
        )
        self.backup_repo.saveJob(auftrag)
        return protokoll

    def _validate(self, import_data, protokoll):
        valid_types = {t.value for t in GeraeteTyp}
        valid_status = {s.value for s in GeraeteStatus}
        seen_ids = set()

        if "geraete" in import_data:
            for i, gd in enumerate(import_data["geraete"]):
                if "name" not in gd or not gd["name"]:
                    protokoll["fehler"].append(f"Geraet {i}: Name fehlt")
                if "typ" not in gd or gd["typ"] not in valid_types:
                    protokoll["fehler"].append(
                        f"Geraet {i}: Ungueltiger Typ '{gd.get('typ')}'"
                    )
                if "status" not in gd or gd["status"] not in valid_status:
                    protokoll["fehler"].append(
                        f"Geraet {i}: Ungueltiger Status '{gd.get('status')}'"
                    )
                if gd.get("status") == "INSTALLIERT" and not gd.get("raumId"):
                    protokoll["fehler"].append(
                        f"Geraet {i}: Installiertes Geraet ohne Raum"
                    )
                if gd.get("status") == "DEFEKT" and gd.get("status") == "INSTALLIERT":
                    protokoll["fehler"].append(
                        f"Geraet {i}: Defektes Geraet darf nicht installiert sein"
                    )
                gid = gd.get("geraetId")
                if gid and gid in seen_ids:
                    protokoll["fehler"].append(
                        f"Geraet {i}: Doppelte ID {gid}"
                    )
                if gid:
                    seen_ids.add(gid)

        if "raeume" in import_data:
            for i, rd in enumerate(import_data["raeume"]):
                if "name" not in rd or not rd["name"]:
                    protokoll["fehler"].append(f"Raum {i}: Name fehlt")
