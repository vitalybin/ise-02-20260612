from enum import Enum


class GeraeteStatus(Enum):
    BESTELLT = "BESTELLT"
    NICHT_INSTALLIERT = "NICHT_INSTALLIERT"
    INSTALLIERT = "INSTALLIERT"
    DEFEKT = "DEFEKT"


class GeraeteTyp(Enum):
    LAMPE = "LAMPE"
    HEIZUNG = "HEIZUNG"
    SENSOR = "SENSOR"
    STECKDOSE = "STECKDOSE"
    KAMERA = "KAMERA"


class Rolle(Enum):
    VIEWER = "VIEWER"
    TECHNIKER = "TECHNIKER"
    ADMIN = "ADMIN"


class Berechtigung(Enum):
    RAUM_LESEN = "RAUM_LESEN"
    GERAET_LESEN = "GERAET_LESEN"
    GERAET_INSTALLIEREN = "GERAET_INSTALLIEREN"
    GERAET_STEUERN = "GERAET_STEUERN"
    GERAET_ERWEITERT_STEUERN = "GERAET_ERWEITERT_STEUERN"
    USER_VERWALTEN = "USER_VERWALTEN"
    DATEN_BACKUP_EXPORT_IMPORT = "DATEN_BACKUP_EXPORT_IMPORT"


ROLLEN_BERECHTIGUNGEN = {
    Rolle.VIEWER: {
        Berechtigung.RAUM_LESEN,
        Berechtigung.GERAET_LESEN,
    },
    Rolle.TECHNIKER: {
        Berechtigung.RAUM_LESEN,
        Berechtigung.GERAET_LESEN,
        Berechtigung.GERAET_INSTALLIEREN,
        Berechtigung.GERAET_STEUERN,
    },
    Rolle.ADMIN: set(Berechtigung),
}
