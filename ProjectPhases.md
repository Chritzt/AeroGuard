📦 Phase 1: Fundament & Architektur-Setup
Das Ziel: Ein sauberes Repository mit Grundgerüst, auf dem wir modular aufbauen können.

🔹 AP 1.1: Repo-Init & Ordnerstruktur
Git Branch: feature/project-setup

Aufgaben:

GitHub-Repository anlegen.

Saubere Ordnerstruktur aufsetzen (/src, /tests, config.py, .gitignore, requirements.txt).

README.md mit einer klaren Kurzbeschreibung anlegen.

Ziel: Basis-Commit pushbar und via Pull Request nach main mergen.

🔹 AP 1.2: Dockerization Core
Git Branch: feature/docker-setup

Aufgaben:

Erstellen eines gehärteten Dockerfile (Multi-Stage Build, Non-Root-User!).

Anlegen einer docker-compose.yml für einfaches lokales Starten mit einem Befehl.

Ziel: Das leere Skript läuft isoliert in Docker.

🛰️ Phase 2: OpenSky Ingestion & Threat Detection Logic
Das Ziel: Echte Live-Flugdaten verarbeiten und Angriffe/Auffälligkeiten erkennen.

🔹 AP 2.1: OpenSky API Ingestion Engine
Git Branch: feature/opensky-ingestion

Aufgaben:

Anbindung an die REST-API von OpenSky Network (mittels requests oder httpx).

Filterung auf ein bestimmtes Geofence (z. B. Luftraum über Österreich / Europa).

Typisierte Daten-Modellierung mittels pydantic (Latitude, Longitude, Altitude, Velocity, Transponder Squawk).

🔹 AP 2.2: Transponder & Emergency Rules (Baseline Detection)
Git Branch: feature/squawk-detector

Aufgaben:

Entwicklung der Regel-Engine für internationale Notfall-Squawks (7700 Emergency, 7600 Radio Loss, 7500 Hijack).

Logging-System aufsetzen (JSON-Format für strukturierte Auswertung).

🔹 AP 2.3: Cyber-Threat Engine (GPS-/ADS-B-Spoofing Detection)
Git Branch: feature/spoofing-detection-engine

Aufgaben:

Velocity & Telemetry Anomaly: Mathematische Prüfung auf unphysikalische Sprünge (z. B. Positionsänderungen, die Überschallgeschwindigkeit erfordern).

Identity Hijacking: Erkennung von doppelt auftretenden ICAO24-Transponder-IDs an zwei verschiedenen Orten.

Berechnung eines dynamischen Threat Scores (0–100) pro Flugobjekt.

🛡️ Phase 3: DevSecOps & Automated Security Gate
Das Ziel: Die automatische Schutzhülle bauen, die deinen Code bei jedem Push sichert.

🔹 AP 3.1: Continuous Integration (CI) & Unit Testing
Git Branch: feature/ci-pytest-pipeline

Aufgaben:

Schreiben von pytest-Tests mit Mocks (gefälschten Flugdaten), um zu prüfen, ob der Spoofing-Detector Notfälle zuverlässig erkennt.

GitHub Action aufsetzen: Automatische Testausführung bei jedem Pull Request.

🔹 AP 3.2: Automated Security Gate (SAST & Secret Scanning)
Git Branch: feature/secops-pipeline

Aufgaben:

Secret Scanner: Gitleaks in GitHub Actions einbauen (blockiert Commits mit harten API-Keys).

SAST (Static Application Security Testing): Integration von Bandit für statische Python-Code-Analyse.

Dependency Audit: Integration von Trivy oder Snyk zur Prüfung von Python-Bibliotheken auf CVEs.

🚀 Phase 4: Integration, Reporting & Portfolio Polish
Das Ziel: Das Projekt visuell und inhaltlich perfekt für Recruiter aufbereiten.

🔹 AP 4.1: Discord / Slack Alerting Webhook
Git Branch: feature/alert-webhook

Aufgaben:

Wenn der Threat Score einen Schwellenwert überschreitet oder ein Notfall-Squawk eingeht, wird automatisch eine strukturierte Alert-Nachricht an einen Discord-/Slack-Channel gesendet.

🔹 AP 4.2: High-Value README & Visual Polish
Git Branch: feature/docs-readme-update

Aufgaben:

AeroGuard Architecture Diagram (mit Mermaid.js oder Draw.io).

Status Badges oben einbauen (CI: Passing, Security Scan: Clean, License: MIT).

"How to Run" in unter 60 Sekunden via Docker.

Kurze Sektion: "Threat Model & Security Considerations".