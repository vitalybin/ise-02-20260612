import json
import os
from datetime import datetime
from domain.repositories import IRaumRepository, IGeraetRepository, IUserRepository, IBackupRepository
from domain.backup_auftrag import BackupAuftrag
from domain.enums import Berechtigung
from application.berechtigungs_service import BerechtigungsService


class DatenBackupService:
    def __init__(self, raum_repo: IRaumRepository, geraet_repo: IGeraetRepository,
                 user_repo: IUserRepository, backup_repo: IBackupRepository,
                 berechtigungs_service: BerechtigungsService,
                 backup_dir: str = "/app/backups"):
        self.raum_repo = raum_repo
        self.geraet_repo = geraet_repo
        self.user_repo = user_repo
        self.backup_repo = backup_repo
        self.berechtigungs_service = berechtigungs_service
        self.backup_dir = backup_dir

    def execute(self, user) -> str:
        self.berechtigungs_service.execute(user, Berechtigung.DATEN_BACKUP_EXPORT_IMPORT)
        os.makedirs(self.backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.json"
        filepath = os.path.join(self.backup_dir, filename)

        raeume = self.raum_repo.findAll()
        geraete = self.geraet_repo.findAll()
        users = self.user_repo.findAll()

        backup_data = {
            "timestamp": timestamp,
            "raeume": [
                {"raumId": r.raumId, "name": r.name, "beschreibung": r.beschreibung}
                for r in raeume
            ],
            "geraete": [
                {
                    "geraetId": g.geraetId, "name": g.name,
                    "typ": g.typ.value, "status": g.status.value,
                    "raumId": g.raumId, "configuration": g.configuration,
                }
                for g in geraete
            ],
            "users": [
                {
                    "userId": u.userId, "username": u.username,
                    "anzeigename": u.anzeigename, "rolle": u.rolle.value,
                    "active": u.active,
                }
                for u in users
            ],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)

        auftrag = BackupAuftrag(
            jobType="backup", filePath=filepath,
            createdBy=user.username, status="erfolgreich"
        )
        self.backup_repo.saveJob(auftrag)
        return filepath
