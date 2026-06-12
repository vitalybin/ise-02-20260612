# Analyse: Navigationsfehler – Ein/Aus im Raum-Detail leitet auf Geräte-Liste um

> **Datum:** 12.06.2026  
> **Projekt:** Smart-Home-Verwaltung (ISE-02 Advanced Programming)  
> **Betroffene Dateien:** `raum_detail.html`, `geraete_controller.py`, `raum_controller.py`

---

## 1. Symptom

**Beobachtetes Verhalten:** Ein Benutzer befindet sich in der Raum-Detail-Ansicht (`/raeume/1`), klickt bei einem installierten Gerät auf „Ein“ oder „Aus“ – und wird **sofort auf die Geräte-Liste (`/geraete`)** umgeleitet, statt auf `/raeume/1` zu bleiben und dort nur den aktualisierten Ein/Aus-Status zu sehen.

**Erwartetes Verhalten:** Die Aktion „Ein/Aus“ soll ausgeführt werden und die Seite soll **auf der aufrufenden Raum-Detail-Seite verbleiben**, mit aktualisiertem Gerätestatus.

---

## 2. Technische Ursache (Root Cause)

### 2.1 Das Formular in der Raum-Detail-View

In `raum_detail.html` (Zeile 30) postet das Ein/Aus-Formular an den **Geräte-Controller**:

```html
<form method="post"
      action="{{ url_for('geraete.steuern', geraet_id=g.geraetId) }}"
      class="d-inline">
```

Das Formular sendet also an die Route `/geraete/<id>/steuern` – **nicht** an eine Route des `RaumController`.

### 2.2 Der Redirect im Geräte-Controller

In `geraete_controller.py` (Zeile 81) endet die `steuern`-Route mit einem **harten Redirect**:

```python
return redirect(url_for("geraete.geraete"))
```

Es gibt:
- ❌ Keinen `redirect_back`-Parameter
- ❌ Keinen `Referer`-Header-Check
- ❌ Keine Fallunterscheidung nach aufrufender Seite

→ **Egal von welcher Seite der Request kommt, es wird immer auf die Geräte-Liste umgeleitet.**

### 2.3 Was im Raum-Controller fehlt

Der `RaumController` (`raum_controller.py`) besitzt **keine eigene Route** für Geräte-Steuerung aus der Raumansicht. Er hat nur:

```python
@raum_bp.route("/raeume/<int:raum_id>")              # GET  – Detailansicht
@raum_bp.route("/raeume/<int:raum_id>/installieren")  # POST – Installation
```

Eine Route wie `/raeume/<int:raum_id>/steuern` existiert **nicht**.

---

## 3. Architektonische Einordnung: Klassendiagramm vs. Verhaltensmodell

### 3.1 Das Klassendiagramm ist unschuldig

Das Klassendiagramm ist ein **Strukturmodell**. Es zeigt:

| Was es zeigt | Bewertung |
|---|---|
| *Welche* Klassen existieren | ✅ Vollständig |
| *Welche* Methoden sie haben | ✅ `+steuern()`, `+konfigurieren()`, `+kalibrieren()` |
| *Welche* Beziehungen bestehen | ✅ Controller ↔ Services ↔ Repositories |
| DDD-Schicht-Zuordnung | ✅ Korrekt |

Was das Klassendiagramm **nicht** spezifiziert (und strukturell auch nicht spezifizieren *kann*):

| Fehlende Information | Wo sie hingehört |
|---|---|
| „Ein/Aus aus der Raum-Detail-Ansicht bleibt auf `/raeume/1`“ | **Sequenzdiagramm** oder **Navigationsmodell** |
| „Der `steuern`-Endpunkt leitet auf die aufrufende Seite zurück“ | **Sequenzdiagramm** (Rückgabepfeil) |
| „`RaumController` braucht eine eigene `steuern`-Route“ | **Use-Case-Realization** / **Verhaltensmodell** |

### 3.2 Was die KI gemacht hat – und was die Aufgabenstellung dazu sagt

Die Aufgabenstellung gibt zur Raumansicht **nur** vor:

> *„In der Raumansicht werden Räume angezeigt. Nach Auswahl eines Raums sollen die dort installierten Geräte sichtbar sein.“*

**Wie** diese „Auswahl“ technisch umgesetzt wird, sagt die Aufgabenstellung **nicht**. Möglichkeiten wären:

| Variante | Beispiel |
|---|---|
| Separate Detailseite | `/raeume/1` – eigene Route mit eigenem Template |
| Expand/Collapse | Alle Räume auf einer Seite, Geräte per Klick ein-/ausklappbar |
| Modal/Dialog | Geräteliste öffnet sich als Overlay |
| AJAX/Inline | Geräte werden per Klick nachgeladen, kein Seitenwechsel |

Die KI hat sich für die **separate Detailseite** (`/raeume/<id>`) entschieden. Das ist eine **Design-Entscheidung**, kein Modell-Fakt. Weder das Klassendiagramm noch die Aufgabenstellung schreiben diese konkrete Umsetzung vor.

Darauf aufbauend hat die KI dann zwei weitere, **UX-seitig falsche** Entscheidungen getroffen:

| Entscheidung | Bewertung |
|---|---|
| **Raum-Detail als eigene Route** (`/raeume/<id>`) | ✅ Plausibles Design, aber nicht modellbasiert – von der KI „ausgedacht“ |
| Existierenden `geraete.steuern`-Endpunkt wiederverwendet | ✅ DRY-Prinzip (Don't Repeat Yourself) |
| Keinen `redirect_back`-Mechanismus eingebaut | ❌ Navigationslogik falsch |
| Keine eigene Route im `RaumController` angelegt | ❌ Fehlende Trennung der View-Kontexte |

**Fazit:** Nicht nur der Redirect ist von der KI erfunden – bereits die **Existenz der Detailseite `/raeume/1`** ist eine KI-Design-Entscheidung, die nicht aus den Modellen ableitbar war. Die Aufgabenstellung sagt *was* passieren soll („installierte Geräte sichtbar“), aber nicht *wie* (Routing, Templates, Navigation). Genau diese Lücke zwischen fachlicher Anforderung und technischer Umsetzung ist der Raum, in dem die KI navigiert – und hier falsch abgebogen ist.

---

## 4. Was hätte den Fehler verhindert?

### 4.1 Ein Sequenzdiagramm für den Flow „Gerät steuern aus Raumansicht“

Hätte das Sequenzdiagramm den Ablauf **aus der Raumansicht heraus** modelliert:

```
User → RaumView (klickt "Ein")
     → RaumController.steuern(geraetId, aktion)
     → GeraetSteuernService.execute(user, geraetId, "einschalten")
     → SqlGeraetRepository.save(geraet)
     ← RaumController: redirect /raeume/<raumId>
     ← RaumView (aktualisiert, zeigt neuen Status)
```

…wäre der Fehler nicht passiert. Die Aufgabenstellung verlangte *mindestens ein* Sequenzdiagramm, aber es wurde keins für genau diesen Flow erstellt.

### 4.2 Explizite Routing-Spezifikation

Eine Tabelle wie:

| Aktion | Ausgangs-View | Ziel-Route | Nach-Aktion-Ziel |
|---|---|---|---|
| Ein/Aus | Raum-Detail | `POST /raeume/<id>/steuern` | `GET /raeume/<id>` |
| Ein/Aus | Geräte-Liste | `POST /geraete/<id>/steuern` | `GET /geraete` |

…hätte den Unterschied zwischen den beiden View-Kontexten klargestellt.

---

## 5. Fazit

| Aspekt | Bewertung |
|---|---|
| **Klassendiagramm** | ✅ Korrekt – Struktur ist vollständig und präzise abgebildet |
| **Verhaltensmodell (Sequenzdiagramm)** | ❌ Fehlte für den Flow „Steuern aus Raumansicht“ |
| **KI-Implementierung** | ⚠️ Architektonisch korrekt (DRY), aber Navigationslogik falsch – kein `redirect_back` |

**Kernaussage:** Das Klassendiagramm war gut genug für die *Struktur*, aber die *Navigation* (welcher Controller-Response auf welche View zurückführt) ist eine **Verhaltensfrage**, die nur ein **Sequenzdiagramm** oder eine **explizite Routing-Spezifikation** klären kann. Strukturmodelle (Klassendiagramme) können Navigationsentscheidungen nicht abbilden – dafür braucht es Verhaltensmodelle.

---

## 6. Mögliche Fix-Strategien (Übersicht)

| Strategie | Beschreibung | Aufwand |
|---|---|---|
| **A: `next`-Parameter** | Formular sendet `?next=/raeume/1` mit; Controller redirected dorthin | Gering |
| **B: Eigene Raum-Route** | `RaumController` bekommt `/raeume/<id>/steuern`-Route | Mittel |
| **C: `Referer`-Check** | Controller prüft `request.referrer` und leitet dorthin zurück | Gering (Security-Risiko) |
| **D: AJAX/Htmx** | Steuerung per AJAX ohne Seiten-Reload | Hoch |
