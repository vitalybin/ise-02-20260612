from domain.repositories import IRaumRepository, IGeraetRepository, IUserRepository, IBackupRepository
from domain.backup_auftrag import BackupAuftrag
from domain.enums import Berechtigung
from application.berechtigungs_service import BerechtigungsService
from infrastructure.json_export_service import JsonExportService
from infrastructure.csv_export_service import CsvExportService


class DatenExportService:
    def __init__(self, raum_repo: IRaumRepository, geraet_repo: IGeraetRepository,
                 user_repo: IUserRepository, backup_repo: IBackupRepository,
                 berechtigungs_service: BerechtigungsService,
                 json_export: JsonExportService, csv_export: CsvExportService,
                 export_dir: str = "/app/exports"):
        self.raum_repo = raum_repo
        self.geraet_repo = geraet_repo
        self.user_repo = user_repo
        self.backup_repo = backup_repo
        self.berechtigungs_service = berechtigungs_service
        self.json_export = json_export
        self.csv_export = csv_export
        self.export_dir = export_dir

    def execute(self, user, export_typ: str = "vollstaendig",
                format: str = "json") -> str:
        self.berechtigungs_service.pruefeBerechtigung(user, Berechtigung.DATEN_BACKUP_EXPORT_IMPORT)

        raeume = self.raum_repo.findAll()
        geraete = self.geraet_repo.findAll()
        users = self.user_repo.findAll()

        data = {}
        if export_typ == "raeume":
            data["raeume"] = [
                {"raumId": r.raumId, "name": r.name, "beschreibung": r.beschreibung}
                for r in raeume
            ]
        elif export_typ == "geraete":
            data["geraete"] = [
                {"geraetId": g.geraetId, "name": g.name, "typ": g.typ.value,
                 "status": g.status.value, "raumId": g.raumId}
                for g in geraete
            ]
        elif export_typ == "defekte_geraete":
            from domain.enums import GeraeteStatus
            defekte = self.geraet_repo.findByStatus(GeraeteStatus.DEFEKT)
            data["defekte_geraete"] = [
                {"geraetId": g.geraetId, "name": g.name, "typ": g.typ.value,
                 "status": g.status.value}
                for g in defekte
            ]
        else:
            data["raeume"] = [
                {"raumId": r.raumId, "name": r.name, "beschreibung": r.beschreibung}
                for r in raeume
            ]
            data["geraete"] = [
                {"geraetId": g.geraetId, "name": g.name, "typ": g.typ.value,
                 "status": g.status.value, "raumId": g.raumId,
                 "configuration": g.configuration}
                for g in geraete
            ]
            data["users"] = [
                {"userId": u.userId, "username": u.username,
                 "anzeigename": u.anzeigename, "rolle": u.rolle.value,
                 "active": u.active}
                for u in users
            ]

        if format == "csv":
            filepath = self.csv_export.export(data, export_typ, self.export_dir)
        else:
            filepath = self.json_export.export(data, export_typ, self.export_dir)

        auftrag = BackupAuftrag(
            jobType="export", filePath=filepath,
            createdBy=user.username, status="erfolgreich"
        )
        self.backup_repo.saveJob(auftrag)
        return filepath
