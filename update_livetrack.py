"""
Automatisches Update-Skript für Garmin Livetrack HTML-Seite
- Fügt aktuelles Datum/Uhrzeit ein
- Aktualisiert LiveTrack-Link aus lokaler Textdatei (garmin_link.txt)
- Kopiert banner.jpg (wenn nötig)
- Commit + Push an GitHub (via Git CLI)
"""

import datetime
import shutil
from pathlib import Path
import subprocess

# === Konfiguration ===
REPO_DIR = Path(__file__).resolve().parent  # Ordner mit Git-Repo
TEMPLATE_FILE = REPO_DIR / "template.html"
OUTPUT_FILE = REPO_DIR / "index.html"
LINK_FILE = REPO_DIR / "garmin_link.txt"
BANNER_FILE = REPO_DIR / "banner.jpeg"

# === Schritt 1: Garmin-Link & Datum laden ===
now = datetime.datetime.now().strftime("%d.%m.%Y, %H:%M Uhr")
try:
    with open(LINK_FILE, "r", encoding="utf-8") as f:
        garmin_link = f.read().strip()
except FileNotFoundError:
    print("⚠️ Datei garmin_link.txt nicht gefunden.")
    garmin_link = "https://livetrack.garmin.com/session/DEIN_LINK"

# === Schritt 2: Template laden & Platzhalter ersetzen ===
with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("##DATETIME##", now)
html = html.replace("DEIN_LINK", garmin_link)

# === Schritt 3: index.html speichern ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ index.html aktualisiert ({now})")

# === Schritt 4: GitHub Commit + Push ===
subprocess.run(["git", "add", "index.html"], cwd=REPO_DIR)
subprocess.run(["git", "add", "banner.jpg"], cwd=REPO_DIR)
subprocess.run(["git", "commit", "-m", f"Auto-Update: {now}"], cwd=REPO_DIR)
subprocess.run(["git", "push"], cwd=REPO_DIR)
