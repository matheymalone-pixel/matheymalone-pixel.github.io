#!/usr/bin/env python3
"""
🛠️ Malone Tools — Barre de menus
Accès rapide à tous vos scripts depuis la barre de menus Mac.
"""

import rumps
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path.home() / "scripts"
PYTHON = str(SCRIPTS_DIR) + "/venv/bin/python3"

class MaloneToolsApp(rumps.App):
    def __init__(self):
        super().__init__("🛠️", quit_button=None)
        self.menu = [
            rumps.MenuItem("🤖 Assistant IA",        callback=self.assistant),
            rumps.MenuItem("📁 Organisateur",         callback=self.organisateur),
            None,  # séparateur
            rumps.MenuItem("🔐 Audit sécurité",       callback=self.audit),
            rumps.MenuItem("🌐 Analyseur réseau",     callback=self.reseau),
            None,  # séparateur
            rumps.MenuItem("🏗️ Nouveau projet",       callback=self.newproject),
            rumps.MenuItem("🎮 Re-Nature",            callback=self.renature),
            None,  # séparateur
            rumps.MenuItem("❌ Quitter",              callback=self.quitter),
        ]

    def lancer(self, commande):
        subprocess.Popen([
            "osascript", "-e",
            f'tell app "Terminal" to do script "{commande}"'
        ])

    def assistant(self, _):
        self.lancer(f"{PYTHON} {SCRIPTS_DIR}/assistant.py")

    def organisateur(self, _):
        self.lancer(f"{PYTHON} {SCRIPTS_DIR}/organiser_telechargements.py")

    def audit(self, _):
        self.lancer(f"{PYTHON} {SCRIPTS_DIR}/security_audit.py")

    def reseau(self, _):
        self.lancer(f"{PYTHON} {SCRIPTS_DIR}/network_analyzer.py")

    def newproject(self, _):
        self.lancer(f"{PYTHON} {SCRIPTS_DIR}/newproject.py")

    def renature(self, _):
        self.lancer(f"cd ~/Re-Nature/sources && {PYTHON} main.py")

    def quitter(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    MaloneToolsApp().run()
