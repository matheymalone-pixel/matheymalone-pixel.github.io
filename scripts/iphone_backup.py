#!/usr/bin/env python3
"""
📱 iPhone Backup Checker — Lemon Tools
Vérifie tes sauvegardes iPhone locales.
"""

import os
import json
import plistlib
from pathlib import Path
from datetime import datetime, timezone

def run(cmd):
    import subprocess
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout.strip()
    except:
        return ""

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "📱 iPhone Backup"\'')

BACKUP_DIR = Path.home() / "Library/Application Support/MobileSync/Backup"

def taille_dossier(path):
    total = 0
    try:
        for f in Path(path).rglob("*"):
            if f.is_file():
                total += f.stat().st_size
    except:
        pass
    gb = total / 1024**3
    mb = total / 1024**2
    return f"{gb:.2f} GB" if gb >= 1 else f"{mb:.0f} MB"

def lire_info_backup(backup_path):
    info_file = Path(backup_path) / "Info.plist"
    manifest_file = Path(backup_path) / "Manifest.plist"
    status_file = Path(backup_path) / "Status.plist"

    info = {}

    try:
        with open(info_file, "rb") as f:
            data = plistlib.load(f)
            info["appareil"] = data.get("Device Name", "iPhone inconnu")
            info["modele"] = data.get("Product Type", "")
            info["ios"] = data.get("Product Version", "")
            info["numero"] = data.get("Phone Number", "")
            last_backup = data.get("Last Backup Date")
            if last_backup:
                info["date"] = last_backup
    except:
        pass

    try:
        with open(manifest_file, "rb") as f:
            data = plistlib.load(f)
            info["chiffre"] = data.get("IsEncrypted", False)
            info["icloud"] = data.get("WasPasscodeSet", False)
    except:
        pass

    try:
        with open(status_file, "rb") as f:
            data = plistlib.load(f)
            info["complete"] = data.get("IsFullBackup", False)
            info["version"] = data.get("Version", "")
    except:
        pass

    return info

def afficher_backups():
    os.system("clear")
    print("\n\033[1;35m  📱  iPhone Backup Checker — Lemon Tools\033[0m")
    print(f"  \033[0;35m{'═' * 48}\033[0m\n")

    if not BACKUP_DIR.exists():
        print("  ❌ Aucune sauvegarde iPhone trouvée")
        print("  💡 Connecte ton iPhone via USB et sauvegarde via Finder")
        return

    backups = [d for d in BACKUP_DIR.iterdir() if d.is_dir()]

    if not backups:
        print("  ❌ Aucune sauvegarde trouvée")
        print(f"  📁 Dossier : {BACKUP_DIR}")
        return

    print(f"  📁 {len(backups)} sauvegarde(s) trouvée(s)\n")

    alertes = []
    now = datetime.now(timezone.utc)

    for i, backup in enumerate(backups, 1):
        info = lire_info_backup(backup)
        taille = taille_dossier(backup)

        print(f"  \033[1;36m{'─' * 48}\033[0m")
        print(f"  📱 Sauvegarde #{i}")
        print(f"  \033[1;37m{info.get('appareil', 'iPhone')}\033[0m  {info.get('modele', '')}")
        print(f"  📱 iOS         : {info.get('ios', '?')}")
        print(f"  📞 Numéro      : {info.get('numero', 'Non disponible')}")
        print(f"  💾 Taille      : {taille}")

        # Date sauvegarde
        date_backup = info.get("date")
        if date_backup:
            if isinstance(date_backup, datetime):
                if date_backup.tzinfo is None:
                    date_backup = date_backup.replace(tzinfo=timezone.utc)
                jours = (now - date_backup).days
                date_str = date_backup.strftime("%d/%m/%Y à %H:%M")

                if jours == 0:
                    age = "\033[1;32mAujourd'hui ✅\033[0m"
                elif jours <= 7:
                    age = f"\033[1;32mIl y a {jours} jour(s) ✅\033[0m"
                elif jours <= 30:
                    age = f"\033[1;33mIl y a {jours} jours ⚠️\033[0m"
                    alertes.append(f"Sauvegarde ancienne — {jours} jours")
                else:
                    age = f"\033[1;31mIl y a {jours} jours 🚨\033[0m"
                    alertes.append(f"Sauvegarde très ancienne — {jours} jours !")

                print(f"  📅 Date        : {date_str}")
                print(f"  ⏱️  Ancienneté  : {age}")

        # Chiffrement
        chiffre = info.get("chiffre", False)
        chiffre_str = "\033[1;32m✅ Chiffrée\033[0m" if chiffre else "\033[1;31m⚠️  Non chiffrée\033[0m"
        print(f"  🔐 Chiffrement : {chiffre_str}")

        # Complète
        complete = info.get("complete", False)
        complete_str = "\033[1;32m✅ Complète\033[0m" if complete else "\033[1;33m⚠️  Incomplète\033[0m"
        print(f"  📦 Type        : {complete_str}")

    print(f"\n  \033[1;36m{'─' * 48}\033[0m")

    if alertes:
        print(f"\n  \033[1;31m⚠️  Alertes :\033[0m")
        for a in alertes:
            print(f"  • {a}")
        notifier(f"⚠️ {alertes[0]}")
    else:
        print(f"\n  \033[1;32m✅ Toutes les sauvegardes sont récentes !\033[0m")
        notifier("✅ Sauvegardes iPhone OK")

    print()

def main():
    afficher_backups()
    input("  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
