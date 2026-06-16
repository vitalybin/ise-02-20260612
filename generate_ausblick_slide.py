"""
Generiert eine Übersichts-Folie: Feature-Priorisierung nach Nutzergruppe
Ausblick für Smart-Home-Verwaltung (ise-02-20260612)
Aktueller Stand: DDD-Architektur, Rollen (Admin/Techniker/Viewer),
CRUD Räume & Geräte, Backup/Export/Import, PostgreSQL, Docker
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12.5)
ax.axis("off")
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#1a1a2e")

# --- Farben ---
COLORS = {
    "Admin": "#1d3557",
    "Techniker": "#e76f51",
    "Bewohner": "#7b2cbf",
    "Gast": "#2d6a4f",
    "Entwickler": "#b07d10",
}

PRIO_COLORS = {
    "Hoch": "#2d6a4f",
    "Mittel": "#b8860b",
    "Niedrig": "#8b0000",
}

STATUS_COLORS = {
    "Neu": "#3a506b",
    "Erweiterung": "#5a189a",
}

# --- Features ---
features = [
    {
        "name": "Automatisierungsregeln",
        "desc": 'Wenn-Dann-Regeln (z.B. "Sensor > 25°C → Heizung aus")',
        "users": ["Bewohner", "Techniker"],
        "prio": "Hoch",
        "status": "Neu",
    },
    {
        "name": "Echtzeit-Dashboard",
        "desc": "Live-Messwerte, Gerätestatus, Raumübersicht",
        "users": ["Bewohner", "Admin"],
        "prio": "Hoch",
        "status": "Neu",
    },
    {
        "name": "Benachrichtigungen & Alarme",
        "desc": "Push/Email bei Defekten, Schwellwertüberschreitungen",
        "users": ["Admin", "Techniker", "Bewohner"],
        "prio": "Hoch",
        "status": "Neu",
    },
    {
        "name": "Zeitsteuerung / Scheduler",
        "desc": "Timer & Zeitpläne für Geräte (Morgens, Abends, etc.)",
        "users": ["Bewohner", "Techniker"],
        "prio": "Hoch",
        "status": "Neu",
    },
    {
        "name": "Szenen & Gerätegruppen",
        "desc": 'Mehrere Geräte gleichzeitig steuern ("Kino-Modus")',
        "users": ["Bewohner", "Gast"],
        "prio": "Mittel",
        "status": "Neu",
    },
    {
        "name": "Logging & Audit-Trail",
        "desc": "Vollständige Aktionsprotokollierung, Fehlerhistorie",
        "users": ["Admin", "Entwickler"],
        "prio": "Mittel",
        "status": "Neu",
    },
    {
        "name": "Energieverbrauch-Tracking",
        "desc": "Stromverbrauch-Statistiken, Graphen, Kostenprognosen",
        "users": ["Bewohner", "Admin"],
        "prio": "Mittel",
        "status": "Neu",
    },
    {
        "name": "REST-API für Drittsysteme",
        "desc": "Externe Integration (Alexa, Google Home, IFTTT)",
        "users": ["Entwickler", "Bewohner"],
        "prio": "Mittel",
        "status": "Erweiterung",
    },
    {
        "name": "Responsive UI / Mobile",
        "desc": "Steuerung vom Smartphone, PWA-Unterstützung",
        "users": ["Bewohner", "Gast"],
        "prio": "Mittel",
        "status": "Erweiterung",
    },
    {
        "name": "Integration Testing / CI",
        "desc": "Automatisierte Tests, Build-Pipeline, Qualitätssicherung",
        "users": ["Entwickler"],
        "prio": "Niedrig",
        "status": "Neu",
    },
    {
        "name": "Multi-Home-Support",
        "desc": "Mehrere Wohnungen/Häuser in einem System verwalten",
        "users": ["Admin", "Bewohner"],
        "prio": "Niedrig",
        "status": "Neu",
    },
    {
        "name": "Gast-Rolle mit Zeitlimit",
        "desc": "Temporäre Zugänge, automatischer Ablauf",
        "users": ["Admin", "Gast"],
        "prio": "Niedrig",
        "status": "Erweiterung",
    },
]

# ============================================================
# TITEL
# ============================================================
ax.text(
    8, 12.1, "Ausblick — Feature-Priorisierung nach Nutzergruppe",
    ha="center", va="center", fontsize=20, fontweight="bold", color="white",
)
ax.text(
    8, 11.65,
    "Smart-Home-Verwaltung  ·  Implementiert: DDD-Architektur, Rollen (Admin/Techniker/Viewer), "
    "CRUD, Backup/Export/Import, Docker + PostgreSQL",
    ha="center", va="center", fontsize=8.5, color="#999999",
)

# ============================================================
# HEADER
# ============================================================
header_y = 11.05
hdr = FancyBboxPatch(
    (0.3, header_y - 0.22), 15.4, 0.5,
    boxstyle="round,pad=0.05", facecolor="#333333", edgecolor="none",
)
ax.add_patch(hdr)
ax.text(3.2, header_y, "Feature", ha="center", va="center",
        fontsize=13, fontweight="bold", color="white")
ax.text(9.2, header_y, "Nutzen für …", ha="center", va="center",
        fontsize=13, fontweight="bold", color="white")
ax.text(13.5, header_y, "Priorität", ha="center", va="center",
        fontsize=13, fontweight="bold", color="white")

# ============================================================
# ZEILEN
# ============================================================
row_h = 0.78
start_y = 10.25

for i, feat in enumerate(features):
    y = start_y - i * row_h

    # Leichte Trennlinie
    ax.plot([0.4, 15.6], [y + 0.38, y + 0.38], color="#2a2a3e", linewidth=0.5)

    # Feature-Name + Beschreibung
    ax.text(0.5, y + 0.05, feat["name"], ha="left", va="center",
            fontsize=11, fontweight="bold", color="white")
    ax.text(0.5, y - 0.25, feat["desc"], ha="left", va="center",
            fontsize=7.5, color="#888888")

    # Status-Badge (Neu / Erweiterung)
    st = feat["status"]
    st_color = STATUS_COLORS.get(st, "#444444")
    st_badge = FancyBboxPatch(
        (5.6, y - 0.13), 1.3, 0.32,
        boxstyle="round,pad=0.06", facecolor=st_color, edgecolor="none", alpha=0.7,
    )
    ax.add_patch(st_badge)
    ax.text(6.25, y + 0.02, st, ha="center", va="center",
            fontsize=7, fontweight="bold", color="white")

    # Nutzergruppen-Badges
    badge_x = 7.3
    for j, user in enumerate(feat["users"]):
        color = COLORS.get(user, "#555555")
        badge = FancyBboxPatch(
            (badge_x + j * 1.65, y - 0.15), 1.5, 0.36,
            boxstyle="round,pad=0.07", facecolor=color, edgecolor="none", alpha=0.9,
        )
        ax.add_patch(badge)
        ax.text(badge_x + j * 1.65 + 0.75, y + 0.02, user,
                ha="center", va="center", fontsize=7.5, fontweight="bold", color="white")

    # Prioritäts-Badge
    prio = feat["prio"]
    prio_color = PRIO_COLORS.get(prio, "#555555")
    prio_badge = FancyBboxPatch(
        (12.9, y - 0.15), 1.3, 0.36,
        boxstyle="round,pad=0.07", facecolor=prio_color, edgecolor="none", alpha=0.9,
    )
    ax.add_patch(prio_badge)
    ax.text(13.55, y + 0.02, prio, ha="center", va="center",
            fontsize=9, fontweight="bold", color="white")

# ============================================================
# LEGENDE
# ============================================================
leg_y = 0.6
ax.text(0.5, leg_y, "Nutzergruppen:", ha="left", va="center",
        fontsize=9, color="#aaaaaa")
lx = 2.5
for label, color in COLORS.items():
    b = FancyBboxPatch(
        (lx, leg_y - 0.15), 1.4, 0.32,
        boxstyle="round,pad=0.06", facecolor=color, edgecolor="none", alpha=0.9,
    )
    ax.add_patch(b)
    ax.text(lx + 0.7, leg_y, label, ha="center", va="center",
            fontsize=8, fontweight="bold", color="white")
    lx += 1.7

# Status-Legende
lx += 0.6
ax.text(lx, leg_y, "Status:", ha="left", va="center",
        fontsize=9, color="#aaaaaa")
lx += 1.2
for label, color in STATUS_COLORS.items():
    b = FancyBboxPatch(
        (lx, leg_y - 0.15), 1.3, 0.32,
        boxstyle="round,pad=0.06", facecolor=color, edgecolor="none", alpha=0.7,
    )
    ax.add_patch(b)
    ax.text(lx + 0.65, leg_y, label, ha="center", va="center",
            fontsize=8, fontweight="bold", color="white")
    lx += 1.6

# ============================================================
# SPEICHERN
# ============================================================
out_path = r"c:\Users\MEURERA\A\ise-02-20260612\Ausblick_Feature_Priorisierung.png"
plt.tight_layout(pad=0.5)
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"Folie gespeichert: {out_path}")
