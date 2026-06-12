# Smart-Home-Verwaltung

Webanwendung zur Verwaltung von Räumen und Smart-Home-Geräten, umgesetzt nach DDD-orientierter Schichtenarchitektur.

## Schnellstart

```powershell
.\start.ps1
```

Die Anwendung ist erreichbar unter: **http://localhost:5000**

### Standard-Zugänge

| Benutzer | Passwort | Rolle |
|---|---|---|
| `admin` | `admin` | ADMIN |
| `techniker` | `techniker` | TECHNIKER |
| `viewer` | `viewer` | VIEWER |

### Stoppen

```powershell
.\stop.ps1
```

## Architektur (DDD-Schichten)

```
┌─────────────────────────────────────────────┐
│ Presentation (UI)                           │
│  LoginController, RaumController,           │
│  GeraeteController, AdminController         │
│  RaumView, GeraeteView, AdminView           │
├─────────────────────────────────────────────┤
│ Application                                 │
│  BerechtigungsService, RaumAnzeigenService,  │
│  GeraetInstallierenService,                 │
│  GeraetSteuernService, ...                  │
├─────────────────────────────────────────────┤
│ Domain                                      │
│  Raum, SmartGeraet, User, BackupAuftrag     │
│  ISmartGeraet, SmartLampe, SmartHeizung,    │
│  SmartSensor, SmartSteckdose, SmartKamera   │
│  SmartGeraetFactory, GeraeteRegelService    │
│  IRaumRepository, IGeraetRepository, ...    │
│  Enums: GeraeteTyp, GeraeteStatus,          │
│         Rolle, Berechtigung                 │
├─────────────────────────────────────────────┤
│ Infrastructure                              │
│  SqlRaumRepository, SqlGeraetRepository,    │
│  SqlUserRepository, SqlBackupRepository     │
│  JsonExportService, CsvExportService,       │
│  ImportService, DatabaseConnection          │
└─────────────────────────────────────────────┘
```

## Projektstruktur

```
code/
├── docker-compose.yml      # Container-Orchestrierung
├── Dockerfile              # App-Container-Definition
├── start.ps1               # Start-Script
├── stop.ps1                # Stop-Script
├── requirements.txt        # Python-Abhängigkeiten
├── db/
│   └── init.sql            # Datenbankschema + Beispieldaten
├── backups/                # Backup-Dateien (Volume)
├── exports/                # Export-Dateien (Volume)
├── imports/                # Import-Dateien (Volume)
└── src/
    ├── app.py              # Hauptanwendung (DI Container)
    ├── domain/             # Fachmodell
    │   ├── enums.py        # GeraeteStatus, GeraeteTyp, Rolle, Berechtigung
    │   ├── raum.py         # Raum Entity
    │   ├── smart_geraet.py # SmartGeraet + ISmartGeraet
    │   ├── smart_lampe.py  # SmartLampe
    │   ├── smart_heizung.py
    │   ├── smart_sensor.py
    │   ├── smart_steckdose.py
    │   ├── smart_kamera.py
    │   ├── user.py         # User Entity
    │   ├── backup_auftrag.py
    │   ├── smart_geraet_factory.py  # Factory Pattern
    │   ├── geraete_regel_service.py # Fachliche Regeln
    │   └── repositories.py # Repository-Interfaces
    ├── application/        # Anwendungsfälle
    │   ├── berechtigungs_service.py
    │   ├── raum_anzeigen_service.py
    │   ├── geraet_anzeigen_service.py
    │   ├── geraet_installieren_service.py
    │   ├── geraet_steuern_service.py
    │   ├── geraet_konfigurieren_service.py
    │   ├── geraet_kalibrieren_service.py
    │   ├── user_verwalten_service.py
    │   ├── daten_backup_service.py
    │   ├── daten_export_service.py
    │   └── daten_import_service.py
    ├── infrastructure/     # Technische Umsetzung
    │   ├── database_connection.py
    │   ├── sql_raum_repository.py
    │   ├── sql_geraet_repository.py
    │   ├── sql_user_repository.py
    │   ├── sql_backup_repository.py
    │   ├── json_export_service.py
    │   ├── csv_export_service.py
    │   └── import_service.py
    └── presentation/       # UI-Schicht
        ├── login_controller.py
        ├── raum_controller.py
        ├── geraete_controller.py
        ├── admin_controller.py
        └── templates/
            ├── base.html
            ├── login.html
            ├── raeume.html
            ├── raum_detail.html
            ├── geraete.html
            └── admin.html
```

## Container & Volumes

| Container | Port | Beschreibung |
|---|---|---|
| `smart-home-app` | 5000 | Flask-Webanwendung |
| `smart-home-db` | 5431 | PostgreSQL 16 Datenbank |

| Volume | Pfad | Beschreibung |
|---|---|---|
| `project-volume` | `./src:/app/src` | Quellcode (Entwicklung) |
| `smart-home-db-volume` | Docker Volume | Persistente DB-Daten |
| `app-exchange-volume` | `./backups, ./exports, ./imports` | Backup/Export/Import |

## Startup-Sequenz (PowerShellScript)

1. **DatabaseConnection erstellen** – Verbindung zu PostgreSQL
2. **SqlRepository erstellen** – Konkrete Repository-Implementierungen
3. **UseCases erstellen** – Application Services mit Dependency Injection
4. **Controller initialisieren** – Flask Blueprints registrieren
5. **App starten** – Flask auf Port 5000

## Technologien

- **Python 3.11** + **Flask 3.0**
- **PostgreSQL 16**
- **Docker / Docker Compose**
- **Bootstrap 5.3** (UI)
- **werkzeug** (Passwort-Hashing)
- **psycopg2** (PostgreSQL-Adapter)

## Daten zurücksetzen

```powershell
docker compose down -v
.\start.ps1
```
