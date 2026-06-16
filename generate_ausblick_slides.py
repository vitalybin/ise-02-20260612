"""
Generiert 3 Präsentationsfolien (16:9) als PNG und PDF für PowerPoint.
Ziel: AMG-nahe Schwarz/Weiß-Optik mit Logo, klarer Typografie und roten Akzenten.

Folie 1: Ausblick auf einen Blick
Folie 2: Feature-Priorisierung nach Nutzergruppe
Folie 3: Roadmap / Ausbaustufen
"""
from __future__ import annotations

import os
from textwrap import fill
from typing import Iterable

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 150
FIGSIZE = (19.2, 10.8)

LOGO_PATH = r"c:\Users\MEURERA\AMG DriveOps\AMG-DriveOps\amg_driveops_flutter\lib\assets\logo.png"

# AMG-like monochrome palette
BG = "#050505"
PANEL = "#101010"
PANEL_2 = "#151515"
PANEL_3 = "#1b1b1b"
WHITE = "#ffffff"
BLACK = "#000000"
GRAY = "#a7a7a7"
MID_GRAY = "#666666"
LIGHT_GRAY = "#d4d4d4"
RED = "#d6001c"
RED_DARK = "#8f0012"
BORDER = "#2a2a2a"
SOFT = "#202020"

USER_COLORS = {
    "Admin": BLACK,
    "Techniker": RED,
    "Bewohner": "#2a2a2a",
    "Gast": "#505050",
    "Entwickler": RED_DARK,
}

PRIO_COLORS = {
    "Hoch": RED,
    "Mittel": "#6a6a6a",
    "Niedrig": "#383838",
}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def make_fig():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 10.8)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    return fig, ax


def save_slide(fig, base_name: str):
    png_path = os.path.join(OUT_DIR, f"{base_name}.png")
    pdf_path = os.path.join(OUT_DIR, f"{base_name}.pdf")
    fig.savefig(png_path, dpi=DPI, facecolor=fig.get_facecolor(), pad_inches=0)
    fig.savefig(pdf_path, facecolor=fig.get_facecolor(), pad_inches=0)
    return png_path, pdf_path


def add_logo(fig):
    if not os.path.exists(LOGO_PATH):
        return
    logo_ax = fig.add_axes([0.80, 0.905, 0.17, 0.07])
    logo_ax.imshow(mpimg.imread(LOGO_PATH))
    logo_ax.axis("off")


def add_header(ax, title: str, subtitle: str = "", title_x: float = 0.9, title_y: float = 10.15):
    ax.text(title_x, title_y, title, ha="left", va="center",
            fontsize=34, fontweight="bold", color=WHITE)
    if subtitle:
        ax.text(title_x, title_y - 0.42, subtitle, ha="left", va="center",
                fontsize=14, color=GRAY)
    line_y = 9.45 if subtitle else 9.7
    ax.plot([title_x, 18.3], [line_y, line_y], color=RED, lw=2.5)


def add_footer(ax, text: str = "Smart-Home-Verwaltung  ·  Ausblick"):
    ax.text(9.6, 0.28, text, ha="center", va="center", fontsize=10.5, color=MID_GRAY)


def badge(ax, x, y, w, h, text, fc, tc=WHITE, ec=BLACK, fs=9.5, weight="bold"):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", facecolor=fc, edgecolor=ec, linewidth=1.0)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, fontweight=weight)


def wrapped(text: str, width: int) -> str:
    return fill(text, width=width, break_long_words=False, break_on_hyphens=False)


def card(ax, x, y, w, h, title, subtitle, bullets: Iterable[str], accent=RED, compact=False):
    bg = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.10",
                        facecolor=PANEL, edgecolor=BORDER, linewidth=1.6)
    ax.add_patch(bg)
    ax.add_patch(Rectangle((x, y + h - 0.10), w, 0.10, facecolor=accent, edgecolor=accent))
    ax.text(x + 0.34, y + h - 0.45, title, ha="left", va="top",
            fontsize=16 if compact else 18, fontweight="bold", color=WHITE)
    if subtitle:
        ax.text(x + 0.34, y + h - 0.88, subtitle, ha="left", va="top",
                fontsize=10.5, color=GRAY)

    top = y + h - (1.55 if not compact else 1.3)
    step = 0.72 if compact else 0.82
    bullet_fs = 10.5 if compact else 11.5
    for i, bullet in enumerate(bullets):
        yy = top - i * step
        ax.text(x + 0.34, yy, "▸", ha="left", va="center", fontsize=15, color=accent)
        ax.text(x + 0.68, yy, bullet, ha="left", va="center", fontsize=bullet_fs, color=WHITE)


# -----------------------------------------------------------------------------
# Slide 1: Overview
# -----------------------------------------------------------------------------
def create_slide1():
    fig, ax = make_fig()
    add_logo(fig)
    add_header(ax, "Ausblick")

    # left side callout
    left = FancyBboxPatch((1.05, 1.55), 7.95, 7.15, boxstyle="round,pad=0.12",
                          facecolor=PANEL_2, edgecolor=BORDER, linewidth=1.4)
    ax.add_patch(left)
    ax.text(5.03, 8.18, "Was wir bereits haben", fontsize=22, fontweight="bold", color=WHITE, ha="center")

    items = [
        ("DDD-Architektur", "Presentation → Application → Domain → Infrastructure"),
        ("Rollen & Rechte", "Admin, Techniker, Viewer"),
        ("CRUD Räume & Geräte", "inkl. Status- und Geräte-Lifecycle"),
        ("Backup / Export / Import", "für Wiederherstellung und Datenübernahme"),
        ("Docker + PostgreSQL", "lauf- und deploybar lokal"),
        ("Web-UI mit Login", "bereits direkt nutzbar"),
    ]
    y = 7.4
    for title, desc in items:
        ax.text(1.48, y, "▸", fontsize=19, color=RED, va="center")
        ax.text(1.82, y, title, fontsize=14.5, fontweight="bold", color=WHITE, va="center")
        ax.text(1.82, y - 0.28, desc, fontsize=11.5, color=LIGHT_GRAY, va="center")
        y -= 0.83

    # center transition
    ax.text(9.6, 5.12, "→", ha="center", va="center", fontsize=42, color=RED)

    # right side callout
    right = FancyBboxPatch((10.2, 1.55), 7.95, 7.15, boxstyle="round,pad=0.12",
                           facecolor=PANEL_3, edgecolor=BORDER, linewidth=1.4)
    ax.add_patch(right)
    ax.text(14.18, 8.18, "Warum genau diese Features?", fontsize=22, fontweight="bold", color=WHITE, ha="center")

    items2 = [
        ("Logging & Audit-Trail", "schnelle Fehlersuche und Transparenz", RED),
        ("Automatisierungsregeln", "echter Smart-Home-Nutzen", WHITE),
        ("Echtzeit-Dashboard", "mehr Überblick für Nutzer", WHITE),
        ("Benachrichtigungen", "aktive Reaktion statt Nachsehen", WHITE),
        ("Skalierung & Komfort", "UI, Mobilität, Multi-Home", WHITE),
    ]
    y = 7.4
    for title, desc, color in items2:
        ax.text(10.62, y, "▸", fontsize=19, color=RED, va="center")
        ax.text(10.96, y, title, fontsize=14.5, fontweight="bold", color=color, va="center")
        ax.text(10.96, y - 0.28, desc, fontsize=11.5, color=LIGHT_GRAY, va="center")
        y -= 0.83

    add_footer(ax)
    path, _ = save_slide(fig, "Ausblick_Folie1_IstStand_vs_Zukunft")
    plt.close()
    return path


# -----------------------------------------------------------------------------
# Slide 2: Priorization
# -----------------------------------------------------------------------------
def create_slide2():
    fig, ax = make_fig()
    add_logo(fig)
    add_header(ax, "Feature-Priorisierung nach Nutzergruppe")

    # left legend rail
    rail_x = 0.95
    rail_y = 1.35
    rail_w = 3.0
    rail_h = 7.35
    rail = FancyBboxPatch((rail_x, rail_y), rail_w, rail_h, boxstyle="round,pad=0.10",
                          facecolor=PANEL_2, edgecolor=BORDER, linewidth=1.4)
    ax.add_patch(rail)
    ax.text(rail_x + rail_w / 2, rail_y + rail_h - 0.28, "Nutzergruppen", fontsize=20, fontweight="bold", color=WHITE, ha="center", va="center")
    ax.plot([rail_x + 0.28, rail_x + rail_w - 0.28], [rail_y + rail_h - 0.58, rail_y + rail_h - 0.58], color=RED, lw=1.4)

    legend_items = [
        ("Admin", "Betrieb, Rechte, Nachvollziehbarkeit"),
        ("Techniker", "Steuern, Setup, Diagnose"),
        ("Bewohner", "Komfort und Alltag"),
        ("Gast", "temporär, eingeschränkt"),
        ("Entwickler", "Wartung, Erweiterung, Integrationen"),
    ]
    y = 7.55
    for label, desc in legend_items:
        badge(ax, 1.25, y - 0.18, 1.25, 0.38, label, USER_COLORS[label], fs=10)
        ax.text(1.25, y - 0.42, wrapped(desc, 20), fontsize=9.5, color=LIGHT_GRAY, va="top", ha="left", linespacing=1.1)
        y -= 1.02

    # Ziel-Callout unten deutlich hervorheben
    ziel_box = FancyBboxPatch(
        (1.15, 1.42),
        2.6,
        0.95,
        boxstyle="round,pad=0.08",
        facecolor=PANEL,
        edgecolor=RED,
        linewidth=1.4,
    )
    ax.add_patch(ziel_box)
    ax.text(1.25, 2.28, "Ziel", fontsize=12.0, color=RED, fontweight="bold", ha="left", va="top")
    ax.text(
        1.25,
        2.02,
        wrapped("Mehr Nutzen fuer Bewohner und Betrieb. System dabei nicht ueberladen.", 22),
        fontsize=8.9,
        color=LIGHT_GRAY,
        ha="left",
        va="top",
        linespacing=1.05,
    )

    columns = [
        ("Hoch", [
            ("Logging & Audit-Trail", "Fehler schneller finden und Aktionen nachvollziehen.", "Admin, Entwickler"),
            ("Automatisierungsregeln", "Bringt den eigentlichen Smart-Home-Mehrwert.", "Bewohner, Techniker"),
            ("Echtzeit-Dashboard", "Sofort sehen, was im Haus passiert.", "Bewohner, Admin"),
            ("Benachrichtigungen & Alarme", "Aktiv reagieren, wenn etwas ausfällt.", "Admin, Techniker, Bewohner"),
        ]),
        ("Mittel", [
            ("Zeitsteuerung / Scheduler", "Zeitpläne und Wiederholungen für Komfort.", "Bewohner, Techniker"),
            ("Szenen & Gerätegruppen", "Mehrere Geräte gemeinsam steuern.", "Bewohner, Gast"),
            ("Energieverbrauch-Tracking", "Transparenz über Verbrauch und Optimierung.", "Bewohner, Admin"),
            ("Responsive Mobile UI", "Bessere Nutzung auf Smartphone und Tablet.", "Bewohner, Gast"),
        ]),
        ("Niedrig", [
            ("REST-API für Drittsysteme", "Später Integration in weitere Ökosysteme.", "Entwickler, Bewohner"),
            ("Multi-Home-Support", "Relevant bei mehreren Häusern oder Standorten.", "Admin, Bewohner"),
            ("Gast-Rolle mit Zeitlimit", "Praktisch, aber kein erster Produkthebel.", "Admin, Gast"),
            ("Fehleranalyse & Tracing", "Ergänzend zu Logging bei weiterem Wachstum.", "Entwickler, Admin"),
        ]),
    ]

    col_x = [4.45, 9.10, 13.75]
    col_w = 4.05
    for idx, (prio, items) in enumerate(columns):
        x = col_x[idx]
        outer = FancyBboxPatch((x, 1.35), col_w, 7.35, boxstyle="round,pad=0.10",
                               facecolor=PANEL_2 if prio == "Hoch" else PANEL,
                               edgecolor=PRIO_COLORS[prio], linewidth=1.5)
        ax.add_patch(outer)
        badge(ax, x + 0.25, 8.1, 1.15, 0.34, prio, PRIO_COLORS[prio], fs=10)

        card_y = 7.72
        for title, desc, users in items:
            inner = FancyBboxPatch((x + 0.18, card_y - 1.31), col_w - 0.36, 1.16, boxstyle="round,pad=0.08",
                                   facecolor=BG, edgecolor=BORDER, linewidth=1.0)
            ax.add_patch(inner)
            ax.text(x + 0.34, card_y - 0.18, wrapped(title, 18), fontsize=12.4, color=WHITE,
                    fontweight="bold", ha="left", va="top", linespacing=1.1)
            ax.text(x + 0.34, card_y - 0.56, wrapped(desc, 20), fontsize=9.6, color=LIGHT_GRAY,
                    ha="left", va="top", linespacing=1.15)
            card_y -= 1.58

    add_footer(ax)
    path, _ = save_slide(fig, "Ausblick_Folie2_Feature_Priorisierung")
    plt.close()
    return path


# -----------------------------------------------------------------------------
# Slide 3: Roadmap
# -----------------------------------------------------------------------------
def create_slide3():
    fig, ax = make_fig()
    add_logo(fig)
    add_header(ax, "Roadmap der nächsten Ausbaustufen")

    phases = [
        {
            "no": "01",
            "title": "Logging & Beobachtbarkeit",
            "accent": RED,
            "bullets": [
                "Fehler- und Ereignisprotokoll",
                "nachvollziehbare Aktionen im Betrieb",
                "schnelleres Debugging und Support",
            ],
            "outcome": "Erhöht Vertrauen und Wartbarkeit",
        },
        {
            "no": "02",
            "title": "Smart-Home-Komfort",
            "accent": RED,
            "bullets": [
                "Automatisierungsregeln und Szenen",
                "Zeitsteuerung, Benachrichtigungen",
                "Dashboard und mobile Nutzung",
            ],
            "outcome": "Macht die Anwendung alltagstauglich",
        },
        {
            "no": "03",
            "title": "Skalierung & Integration",
            "accent": "#7a7a7a",
            "bullets": [
                "REST-API und externe Systeme",
                "Multi-Home und Gastzugänge",
                "Performance- und Tracing-Ausbau",
            ],
            "outcome": "Bereitet Wachstum und produktiven Betrieb vor",
        },
    ]

    box_w = 4.6
    box_h = 6.95
    gap = 0.95
    total_width = (3 * box_w) + (2 * gap)
    start_x = (19.2 - total_width) / 2
    x_positions = [start_x, start_x + box_w + gap, start_x + (2 * (box_w + gap))]
    for idx, phase in enumerate(phases):
        x = x_positions[idx]
        box = FancyBboxPatch((x, 1.55), box_w, box_h, boxstyle="round,pad=0.12",
                             facecolor=PANEL_2 if idx == 0 else PANEL if idx == 1 else PANEL_3,
                             edgecolor=phase["accent"], linewidth=1.8)
        ax.add_patch(box)

        badge(ax, x + 0.34, 7.92, 0.78, 0.42, phase["no"], phase["accent"], fs=19)
        ax.text(x + 0.34, 7.48, wrapped(phase["title"], 18), fontsize=15.5, fontweight="bold", color=WHITE, ha="left", va="top", linespacing=1.02)

        yy = 5.95
        for bullet in phase["bullets"]:
            ax.text(x + 0.28, yy, "▸", fontsize=18, color=phase["accent"], va="center")
            ax.text(x + 0.56, yy, bullet, fontsize=13.5, color=WHITE, va="center")
            yy -= 0.72

        ax.add_patch(FancyBboxPatch((x + 0.28, 2.03), box_w - 0.56, 0.92, boxstyle="round,pad=0.10",
                                     facecolor=BG, edgecolor=BORDER, linewidth=1.0))
        ax.text(x + (box_w / 2), 2.49, phase["outcome"], fontsize=12, color=LIGHT_GRAY,
                ha="center", va="center", wrap=True)

    # arrows between phases
    arrow_1_x = x_positions[0] + box_w + (gap / 2)
    arrow_2_x = x_positions[1] + box_w + (gap / 2)
    ax.text(arrow_1_x, 5.0, "→", fontsize=34, color=MID_GRAY, va="center", ha="center")
    ax.text(arrow_2_x, 5.0, "→", fontsize=34, color=MID_GRAY, va="center", ha="center")

    # KPI-Block als messbarer Ausblick (kompakt und ohne unklare Abkürzungen)
    kpi_box = FancyBboxPatch(
        (4.7, 0.62),
        9.8,
        0.78,
        boxstyle="round,pad=0.08",
        facecolor=PANEL,
        edgecolor=RED,
        linewidth=1.2,
    )
    ax.add_patch(kpi_box)
    ax.text(4.95, 1.18, "KPI-Ziele (12 Monate)", fontsize=11.5, color=RED, fontweight="bold", ha="left", va="center")
    ax.text(
        4.95,
        0.86,
        "Durchschnittliche Entstoerungszeit -30% | Zeit bis Fehlerursache -25% | Automatisierungsquote >40% | Nutzerzufriedenheit +20% (Umfrage-Score ggü. Projektstart)",
        fontsize=9.4,
        color=LIGHT_GRAY,
        ha="left",
        va="center",
    )

    add_footer(ax)
    path, _ = save_slide(fig, "Ausblick_Folie3_Roadmap")
    plt.close()
    return path


# -----------------------------------------------------------------------------
# Slide 4: Risiken & Gegenmaßnahmen
# -----------------------------------------------------------------------------
def create_slide4():
    fig, ax = make_fig()
    add_logo(fig)
    add_header(ax, "Risiken und Gegenmaßnahmen")

    risks = [
        {
            "risk": "Komplexität der Automatisierungsregeln steigt schnell",
            "impact": "Inkonsistente Regeln, schwer nachvollziehbares Verhalten",
            "mitigation": "Regel-Templates, Testfälle pro Regel, Freigabeprozess",
            "prio": "Hoch",
        },
        {
            "risk": "Betriebsfehler werden zu spät erkannt",
            "impact": "Längere Ausfallzeiten und langsame Problemlösung",
            "mitigation": "Logging zuerst, Alerting-Schwellen, Incident-Runbook",
            "prio": "Hoch",
        },
        {
            "risk": "Feature-Wunschliste überlädt das Produkt",
            "impact": "Verzögerungen, sinkende Qualität, unklarer Fokus",
            "mitigation": "Quartalsweise Priorisierung nach Nutzen und Aufwand",
            "prio": "Mittel",
        },
        {
            "risk": "Skalierungsthemen kommen zu spät auf den Tisch",
            "impact": "Performance-Engpässe bei mehr Geräten/Haushalten",
            "mitigation": "Frühe Lasttests, API-Grenzen, Monitoring-KPIs",
            "prio": "Mittel",
        },
    ]

    left_x = 1.0
    right_x = 10.05
    card_w = 8.15
    card_h = 3.25

    for idx, entry in enumerate(risks):
        row = idx // 2
        col = idx % 2
        x = left_x if col == 0 else right_x
        y = 8.8 - (row * 3.7)

        card = FancyBboxPatch(
            (x, y - card_h),
            card_w,
            card_h,
            boxstyle="round,pad=0.10",
            facecolor=PANEL_2 if entry["prio"] == "Hoch" else PANEL,
            edgecolor=RED if entry["prio"] == "Hoch" else BORDER,
            linewidth=1.5,
        )
        ax.add_patch(card)

        badge(ax, x + card_w - 1.45, y - 0.48, 1.15, 0.30, entry["prio"], RED if entry["prio"] == "Hoch" else MID_GRAY, fs=9.0)

        ax.text(x + 0.25, y - 0.38, "Risiko", fontsize=10.5, color=RED, fontweight="bold", ha="left", va="center")
        ax.text(x + 0.25, y - 0.72, wrapped(entry["risk"], 38), fontsize=11.3, color=WHITE, fontweight="bold", ha="left", va="top", linespacing=1.08)

        ax.text(x + 0.25, y - 1.56, "Auswirkung", fontsize=10.0, color=GRAY, fontweight="bold", ha="left", va="center")
        ax.text(x + 0.25, y - 1.84, wrapped(entry["impact"], 40), fontsize=10.0, color=LIGHT_GRAY, ha="left", va="top", linespacing=1.08)

        ax.text(x + 0.25, y - 2.42, "Gegenmaßnahme", fontsize=10.0, color=GRAY, fontweight="bold", ha="left", va="center")
        ax.text(x + 0.25, y - 2.70, wrapped(entry["mitigation"], 40), fontsize=10.0, color=LIGHT_GRAY, ha="left", va="top", linespacing=1.08)

    add_footer(ax)
    path, _ = save_slide(fig, "Ausblick_Folie4_Risiken_Gegenmassnahmen")
    plt.close()
    return path


if __name__ == "__main__":
    print("Generiere Ausblick-Folien im AMG-Stil ...\n")
    paths = [create_slide1(), create_slide2(), create_slide3(), create_slide4()]
    print("\nFertig:")
    for idx, path in enumerate(paths, start=1):
        print(f"  {idx}) {os.path.basename(path)}")
