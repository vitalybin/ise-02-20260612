-- =====================================================
-- Smart-Home-Verwaltung - Datenbankinitialisierung
-- PostgreSQL 16
-- =====================================================

-- Tabelle: rooms
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT DEFAULT ''
);

-- Tabelle: devices (Single-Table-Inheritance)
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'NICHT_INSTALLIERT',
    room_id INTEGER REFERENCES rooms(id) ON DELETE SET NULL,
    configuration JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabelle: users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'VIEWER',
    active BOOLEAN DEFAULT true
);

-- Tabelle: backup_jobs
CREATE TABLE IF NOT EXISTS backup_jobs (
    id SERIAL PRIMARY KEY,
    job_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(512),
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'erfolgreich'
);

-- =====================================================
-- Beispieldaten: Raeume
-- =====================================================
INSERT INTO rooms (name, description) VALUES
    ('Wohnzimmer', 'Hauptwohnbereich mit Fernseher und Sofa'),
    ('Kueche', 'Kochbereich mit Kochinsel'),
    ('Schlafzimmer', 'Schlafbereich im Obergeschoss'),
    ('Badezimmer', 'Bad mit Dusche und Badewanne'),
    ('Buero', 'Arbeitszimmer mit Schreibtisch'),
    ('Flur', 'Eingangsbereich');

-- =====================================================
-- Beispieldaten: Geraete
-- =====================================================
INSERT INTO devices (name, device_type, status, room_id, configuration) VALUES
    ('Deckenlampe Wohnzimmer', 'LAMPE', 'INSTALLIERT', 1, '{"helligkeit": 100, "farbe": "weiss", "eingeschaltet": true}'),
    ('Stehlampe Wohnzimmer', 'LAMPE', 'INSTALLIERT', 1, '{"helligkeit": 80, "farbe": "warmweiss", "eingeschaltet": false}'),
    ('Heizung Wohnzimmer', 'HEIZUNG', 'INSTALLIERT', 1, '{"zieltemperatur": 21.0, "eingeschaltet": true}'),
    ('Temperatursensor Kueche', 'SENSOR', 'INSTALLIERT', 2, '{"messwert": 22.5, "einheit": "°C", "kalibriert": true}'),
    ('Kaffeemaschinen-Steckdose', 'STECKDOSE', 'INSTALLIERT', 2, '{"stromverbrauch": 1200, "eingeschaltet": true}'),
    ('Ueberwachungskamera Flur', 'KAMERA', 'INSTALLIERT', 6, '{"modus": "normal", "eingeschaltet": true}'),
    ('Heizung Schlafzimmer', 'HEIZUNG', 'INSTALLIERT', 3, '{"zieltemperatur": 19.0, "eingeschaltet": true}'),
    ('Badezimmer-Lampe', 'LAMPE', 'INSTALLIERT', 4, '{"helligkeit": 70, "farbe": "weiss", "eingeschaltet": false}'),
    ('Smart-Thermostat', 'HEIZUNG', 'NICHT_INSTALLIERT', NULL, '{"zieltemperatur": 20.0}'),
    ('Neue Deckenlampe', 'LAMPE', 'BESTELLT', NULL, '{}'),
    ('Defekter Bewegungssensor', 'SENSOR', 'DEFEKT', NULL, '{"messwert": 0, "einheit": "Bewegung"}'),
    ('Gartensteckdose', 'STECKDOSE', 'NICHT_INSTALLIERT', NULL, '{"stromverbrauch": 0}');
