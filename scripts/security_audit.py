#!/usr/bin/env python3
"""
🔐 Mac Security Audit
Scanne votre Mac et génère un rapport de sécurité.
Auteur : Malone | Usage : python3 security_audit.py
"""

import os
import sys
import json
import subprocess
import socket
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────

EXTENSIONS_SUSPECTES = [
    ".exe", ".bat", ".cmd", ".vbs", ".scr",      # Windows sur Mac = suspect
    ".sh",                                          # Scripts shell cachés
]

EXTENSIONS_TROMPEUSES = [
    (".jpg.py", "⚠️  Faux fichier image"),
    (".pdf.sh", "⚠️  Faux PDF"),
    (".png.exe", "⚠️  Faux image"),
    (".mp4.py", "⚠️  Fausse vidéo"),
]

PROCESSUS_LEGIT = [
    "python", "python3", "bash", "zsh", "ssh", "git",
    "node", "npm", "brew", "curl", "wget", "vim", "nano",
    "finder", "dock", "spotlight", "coreaudiod", "kernel",
    "loginwindow", "launchd", "windowserver", "mds", "mdworker",
    "com.apple", "safari", "chrome", "firefox", "code", "slack",
    "terminal", "iterm", "xcode", "activity", "system"
]

DOSSIERS_A_SCANNER = [
    Path.home() / "Downloads",
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Library" / "LaunchAgents",
]

RAPPORT_SORTIE = Path.home() / "Desktop" / f"audit_securite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# ─────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────

resultats = {
    "safe":     [],
    "warning":  [],
    "danger":   [],
}

def log(niveau, categorie, message):
    icone = {"safe": "✅", "warning": "⚠️ ", "danger": "🚨"}[niveau]
    print(f"  {icone} [{categorie}] {message}")
    resultats[niveau].append(f"{icone} [{categorie}] {message}")

def titre(texte):
    print(f"\n{'─'*50}")
    print(f"  🔍 {texte}")
    print(f"{'─'*50}")

def run(commande):
    """Lance une commande shell et retourne la sortie."""
    try:
        result = subprocess.run(
            commande, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return ""

# ─────────────────────────────────────────
# 1. FICHIERS ET EXTENSIONS SUSPECTES
# ─────────────────────────────────────────

def scanner_fichiers():
    titre("Fichiers et extensions suspectes")

    for dossier in DOSSIERS_A_SCANNER:
        if not dossier.exists():
            continue

        try:
            fichiers = list(dossier.rglob("*"))
        except PermissionError:
            continue

        for fichier in fichiers:
            if not fichier.is_file():
                continue

            nom = fichier.name
            suffixe = fichier.suffix.lower()

            # Extensions Windows sur Mac
            if suffixe in EXTENSIONS_SUSPECTES:
                log("danger", "Extension", f"{fichier} → extension suspecte sur Mac '{suffixe}'")
                continue

            # Extensions trompeuses (double extension)
            for double_ext, raison in EXTENSIONS_TROMPEUSES:
                if nom.lower().endswith(double_ext):
                    log("danger", "Extension trompeuse", f"{fichier} → {raison}")
                    continue

            # Fichiers cachés dans Downloads/Desktop
            if nom.startswith(".") and dossier in [
                Path.home() / "Downloads",
                Path.home() / "Desktop"
            ]:
                log("warning", "Fichier caché", f"{fichier}")
                continue

            # Fichiers exécutables dans Downloads
            if os.access(fichier, os.X_OK) and dossier == Path.home() / "Downloads":
                log("warning", "Exécutable", f"{fichier} → fichier exécutable dans Téléchargements")

    # LaunchAgents — scripts de démarrage
    launch_agents = Path.home() / "Library" / "LaunchAgents"
    if launch_agents.exists():
        agents = list(launch_agents.glob("*.plist"))
        if agents:
            for agent in agents:
                if any(legit in agent.name.lower() for legit in ["com.apple", "homebrew", "google", "adobe", "microsoft"]):
                    log("safe", "LaunchAgent", f"{agent.name}")
                else:
                    log("warning", "LaunchAgent inconnu", f"{agent.name} → vérifiez si vous connaissez cette app")
        else:
            log("safe", "LaunchAgents", "Aucun agent de démarrage suspect trouvé")

# ─────────────────────────────────────────
# 2. APPLICATIONS AU DÉMARRAGE
# ─────────────────────────────────────────

def scanner_demarrage():
    titre("Applications au démarrage (Login Items)")

    # Via sfltool (liste les login items)
    output = run("osascript -e 'tell application \"System Events\" to get the name of every login item'")

    if output:
        items = [i.strip() for i in output.split(",")]
        for item in items:
            item_lower = item.lower()
            if any(legit in item_lower for legit in [
                "dropbox", "google", "spotify", "1password", "alfred",
                "bartender", "cleanmymac", "amphetamine", "istat", "karabiner",
                "rectangle", "magnet", "notion", "slack", "zoom", "discord",
                "raycast", "iterm", "apple"
            ]):
                log("safe", "Démarrage", f"{item} → application connue")
            else:
                log("warning", "Démarrage inconnu", f"{item} → vérifiez si vous avez installé cette app")
    else:
        log("safe", "Démarrage", "Impossible de lire les login items (normal sans permissions)")

    # LaunchDaemons système
    daemons = run("ls /Library/LaunchDaemons/ 2>/dev/null")
    if daemons:
        for daemon in daemons.split("\n")[:10]:
            if any(legit in daemon.lower() for legit in ["com.apple", "homebrew", "adobe", "microsoft", "google"]):
                log("safe", "Daemon", daemon)
            else:
                log("warning", "Daemon inconnu", f"{daemon} → service système non standard")

# ─────────────────────────────────────────
# 3. PROCESSUS EN COURS
# ─────────────────────────────────────────

def scanner_processus():
    titre("Processus en cours d'exécution")

    output = run("ps aux")
    lignes = output.split("\n")[1:]  # Ignore l'en-tête

    suspects = []
    for ligne in lignes:
        if not ligne.strip():
            continue
        parties = ligne.split()
        if len(parties) < 11:
            continue

        utilisateur = parties[0]
        cpu = float(parties[2]) if parties[2].replace(".", "").isdigit() else 0
        memoire = float(parties[3]) if parties[3].replace(".", "").isdigit() else 0
        commande = " ".join(parties[10:]).lower()

        # Processus avec CPU très élevé
        if cpu > 50:
            log("warning", "CPU élevé", f"{commande[:60]} → {cpu}% CPU")
            continue

        # Processus root non Apple
        if utilisateur == "root" and not any(l in commande for l in ["com.apple", "kernel", "launchd", "system"]):
            if cpu > 5:
                log("warning", "Processus root", f"{commande[:60]}")
            continue

        # Processus Python/Shell inconnus
        if any(x in commande for x in ["python", "python3", "bash", "sh "]):
            if "security_audit" not in commande and "organiser" not in commande:
                if not any(l in commande for l in PROCESSUS_LEGIT):
                    suspects.append(commande[:60])

    if suspects:
        for s in suspects[:5]:
            log("warning", "Script actif", s)
    else:
        log("safe", "Processus", "Aucun script suspect détecté en arrière-plan")

    # Processus qui écoutent sur le réseau
    ports = run("lsof -i -n -P 2>/dev/null | grep LISTEN")
    if ports:
        lignes_ports = ports.split("\n")
        for ligne in lignes_ports[:15]:
            if any(legit in ligne.lower() for legit in [
                "python", "node", "ruby", "php", "nginx", "apache",
                "com.apple", "rapportd", "identitys", "configd"
            ]):
                log("safe", "Port ouvert", ligne.split()[-1] if ligne.split() else ligne)
            else:
                log("warning", "Port ouvert", f"{ligne[:80]}")

# ─────────────────────────────────────────
# 4. CONNEXIONS RÉSEAU ACTIVES
# ─────────────────────────────────────────

def scanner_reseau():
    titre("Connexions réseau actives")

    # Connexions établies
    output = run("lsof -i -n -P 2>/dev/null | grep ESTABLISHED")
    if not output:
        log("safe", "Réseau", "Aucune connexion sortante suspecte détectée")
        return

    domaines_legit = [
        "apple.com", "icloud.com", "google.com", "googleapis.com",
        "cloudflare.com", "github.com", "amazonaws.com", "akamai",
        "cdn", "spotify.com", "slack.com", "discord.com", "notion.so",
        "anthropic.com", "openai.com", "localhost", "127.0.0.1"
    ]

    connexions_vues = set()
    for ligne in output.split("\n"):
        if not ligne.strip():
            continue
        parties = ligne.split()
        if len(parties) < 9:
            continue

        app = parties[0]
        adresse = parties[-2] if len(parties) > 2 else "?"

        cle = f"{app}:{adresse}"
        if cle in connexions_vues:
            continue
        connexions_vues.add(cle)

        if any(legit in adresse.lower() for legit in domaines_legit):
            log("safe", "Connexion", f"{app} → {adresse}")
        else:
            log("warning", "Connexion inconnue", f"{app} → {adresse}")

# ─────────────────────────────────────────
# 5. RAPPORT FINAL
# ─────────────────────────────────────────

def generer_rapport():
    titre("RAPPORT DE SÉCURITÉ")

    total_danger  = len(resultats["danger"])
    total_warning = len(resultats["warning"])
    total_safe    = len(resultats["safe"])
    total         = total_danger + total_warning + total_safe

    print(f"""
  📊 Résumé
  {'─'*30}
  🚨 Dangers   : {total_danger}
  ⚠️  Avertiss. : {total_warning}
  ✅ Safe      : {total_safe}
  📁 Total     : {total} éléments analysés
    """)

    if total_danger == 0 and total_warning == 0:
        print("  🎉 Excellent ! Votre Mac semble sain.")
    elif total_danger == 0:
        print("  👍 Pas de danger critique — quelques points à vérifier manuellement.")
    else:
        print("  ⛔ Des éléments critiques ont été trouvés — vérifiez les 🚨 ci-dessus.")

    # Sauvegarde du rapport
    with open(RAPPORT_SORTIE, "w", encoding="utf-8") as f:
        f.write(f"🔐 Rapport d'audit Mac — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 50 + "\n\n")
        for niveau in ["danger", "warning", "safe"]:
            if resultats[niveau]:
                f.write(f"\n{'🚨 DANGERS' if niveau == 'danger' else '⚠️  AVERTISSEMENTS' if niveau == 'warning' else '✅ SAFE'}\n")
                f.write("─" * 30 + "\n")
                for ligne in resultats[niveau]:
                    f.write(ligne + "\n")

    print(f"\n  📄 Rapport sauvegardé sur votre Bureau :\n  {RAPPORT_SORTIE}\n")

# ─────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("\n🔐 Mac Security Audit — by Malone")
    print("=" * 50)
    print("  ⏳ Scan en cours, patientez...\n")

    scanner_fichiers()
    scanner_demarrage()
    scanner_processus()
    scanner_reseau()
    generer_rapport()
