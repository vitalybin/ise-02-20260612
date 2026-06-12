"""
Smart-Home-Verwaltung - Hauptanwendung

PowerShellScript-Äquivalent (DI Container / Startup):
  -> DatabaseConnection erstellen
  -> SqlRepository erstellen
  -> UseCases erstellen
  -> Controller initialisieren
  -> App starten
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, redirect, url_for
from werkzeug.security import generate_password_hash

# Infrastructure
from infrastructure.database_connection import DatabaseConnection
from infrastructure.sql_raum_repository import SqlRaumRepository
from infrastructure.sql_geraet_repository import SqlGeraetRepository
from infrastructure.sql_user_repository import SqlUserRepository
from infrastructure.sql_backup_repository import SqlBackupRepository
from infrastructure.json_export_service import JsonExportService
from infrastructure.csv_export_service import CsvExportService
from infrastructure.import_service import ImportService

# Domain
from domain.geraete_regel_service import GeraeteRegelService

# Application (UseCases / Services)
from application.berechtigungs_service import BerechtigungsService
from application.raum_anzeigen_service import RaumAnzeigenService
from application.geraet_anzeigen_service import GeraetAnzeigenService
from application.geraet_installieren_service import GeraetInstallierenService
from application.geraet_steuern_service import GeraetSteuernService
from application.geraet_konfigurieren_service import GeraetKonfigurierenService
from application.geraet_kalibrieren_service import GeraetKalibrierenService
from application.user_verwalten_service import UserVerwaltenService
from application.daten_backup_service import DatenBackupService
from application.daten_export_service import DatenExportService
from application.daten_import_service import DatenImportService

# Presentation (Controller)
from presentation.login_controller import LoginController
from presentation.raum_controller import RaumController
from presentation.geraete_controller import GeraeteController
from presentation.admin_controller import AdminController


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "presentation", "templates"),
    )
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

    # --- 1. DatabaseConnection erstellen ---
    db = DatabaseConnection()

    # --- 2. SqlRepository erstellen ---
    raum_repo = SqlRaumRepository(db)
    geraet_repo = SqlGeraetRepository(db)
    user_repo = SqlUserRepository(db)
    backup_repo = SqlBackupRepository(db)
    json_export = JsonExportService()
    csv_export = CsvExportService()
    import_service = ImportService()

    # Domain Services
    regel_service = GeraeteRegelService()

    # --- 3. UseCases erstellen ---
    berechtigungs_service = BerechtigungsService()
    raum_anzeigen = RaumAnzeigenService(raum_repo, geraet_repo, berechtigungs_service)
    geraet_anzeigen = GeraetAnzeigenService(geraet_repo, berechtigungs_service)
    geraet_installieren = GeraetInstallierenService(
        geraet_repo, raum_repo, regel_service, berechtigungs_service
    )
    geraet_steuern = GeraetSteuernService(geraet_repo, regel_service, berechtigungs_service)
    geraet_konfigurieren = GeraetKonfigurierenService(
        geraet_repo, regel_service, berechtigungs_service
    )
    geraet_kalibrieren = GeraetKalibrierenService(
        geraet_repo, regel_service, berechtigungs_service
    )
    user_verwalten = UserVerwaltenService(user_repo, berechtigungs_service)
    daten_backup = DatenBackupService(
        raum_repo, geraet_repo, user_repo, backup_repo, berechtigungs_service
    )
    daten_export = DatenExportService(
        raum_repo, geraet_repo, user_repo, backup_repo,
        berechtigungs_service, json_export, csv_export
    )
    daten_import = DatenImportService(
        raum_repo, geraet_repo, backup_repo, berechtigungs_service
    )

    # --- 4. Controller initialisieren ---
    login_ctrl = LoginController(user_repo)
    raum_ctrl = RaumController(raum_anzeigen, geraet_installieren, user_repo)
    geraete_ctrl = GeraeteController(
        geraet_anzeigen, geraet_steuern, geraet_konfigurieren,
        geraet_kalibrieren, raum_anzeigen, geraet_repo, user_repo
    )
    admin_ctrl = AdminController(
        user_verwalten, daten_backup, daten_export, daten_import,
        backup_repo, import_service, user_repo
    )

    login_ctrl.register(app)
    raum_ctrl.register(app)
    geraete_ctrl.register(app)
    admin_ctrl.register(app)

    # Seed default users on first start
    _seed_default_users(user_repo)

    return app


def _seed_default_users(user_repo):
    """Erzeugt Standard-Benutzer falls die Datenbank leer ist."""
    from domain.user import User
    from domain.enums import Rolle

    try:
        existing = user_repo.findByUsername("admin")
        if existing:
            return

        defaults = [
            ("admin", "admin", "Administrator", Rolle.ADMIN),
            ("techniker", "techniker", "Max Techniker", Rolle.TECHNIKER),
            ("viewer", "viewer", "Lisa Viewer", Rolle.VIEWER),
        ]
        for username, password, name, rolle in defaults:
            user = User(
                username=username,
                passwordHash=generate_password_hash(password),
                anzeigename=name,
                rolle=rolle,
                active=True,
            )
            user_repo.save(user)
    except Exception as e:
        print(f"Warnung: Seed-Daten konnten nicht erstellt werden: {e}")


# --- 5. App starten ---
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
