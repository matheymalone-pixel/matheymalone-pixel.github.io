#!/usr/bin/env python3
"""
🔍 Process Monitor — Lemon Tools
Surveille les processus suspects sur ton Mac.
"""

import subprocess
import os
from datetime import datetime

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "🔍 Process Monitor"\'')

# Processus légitimes connus
PROCESSUS_SAFE = [
    "kernel_task", "launchd", "WindowServer", "Safari", "Chrome", "Firefox",
    "Code", "iTerm2", "Terminal", "Finder", "Dock", "SystemUIServer",
    "python3", "python", "node", "git", "zsh", "bash", "ssh",
    "Spotify", "Discord", "Slack", "zoom", "Messages", "Mail",
    "Photos", "Music", "Calendar", "Notes", "Xcode", "Activity Monitor",
    "coreaudiod", "logd", "configd", "diskarbitrationd", "sharingd",
    "mds", "mdworker", "Spotlight", "cfprefsd", "opendirectoryd",
]

# Noms suspects
NOMS_SUSPECTS = [
    "miner", "crypto", "xmrig", "monero", "bitcoin", "coinminer",
    "backdoor", "rootkit", "keylog", "spyware", "trojan", "malware",
    "netcat", "ncat", "reverse", "shell", "exploit", "payload",
    "darkcomet", "njrat", "remcos", "asyncrat",
]

# Seuils d'alerte
CPU_SEUIL = 80
RAM_SEUIL = 1000  # MB

def get_processus():
    output = run("ps aux | sort -rk 3 | head -40")
    processus = []
    for ligne in output.splitlines()[1:]:
        parts = ligne.split()
        if len(parts) < 11:
            continue
        try:
            user = parts[0]
            pid = parts[1]
            cpu = float(parts[2])
            mem_mb = float(parts[3]) * 0.01 * 16000  # estimation RAM
            nom = os.path.basename(parts[10])
            processus.append({
                "user": user,
                "pid": pid,
                "cpu": cpu,
                "ram": round(mem_mb),
                "nom": nom,
                "cmd": " ".join(parts[10:])[:60],
            })
        except:
            continue
    return processus

def analyser_processus(p):
    nom_lower = p["nom"].lower()
    cmd_lower = p["cmd"].lower()

    # Suspect par nom
    for suspect in NOMS_SUSPECTS:
        if suspect in nom_lower or suspect in cmd_lower:
            return "DANGER", "\033[1;31m"

    # CPU très élevé
    if p["cpu"] > CPU_SEUIL:
        return "CPU ÉLEVÉ", "\033[1;33m"

    # RAM très élevée
    if p["ram"] > RAM_SEUIL:
        return "RAM ÉLEVÉE", "\033[1;33m"

    # Processus inconnu qui tourne en root
    if p["user"] == "root" and p["nom"] not in PROCESSUS_SAFE:
        return "ROOT INCONNU", "\033[1;33m"

    return "Normal", "\033[1;32m"

def afficher_processus(processus):
    reset = "\033[0m"
    print(f"\n  {'─'*65}")
    print(f"  {'NOM':<22} {'PID':<8} {'CPU':<8} {'RAM':<12} STATUT")
    print(f"  {'─'*65}")

    suspects = []
    for p in processus:
        statut, couleur = analyser_processus(p)

        if statut != "Normal":
            suspects.append(p)
            emoji = "⚠️ " if statut != "DANGER" else "🚨"
        else:
            emoji = "✅"

        cpu_str = f"{p['cpu']:.1f}%"
        ram_str = f"{p['ram']}MB"

        print(f"  {emoji} {p['nom']:<20} {p['pid']:<8} {cpu_str:<8} {ram_str:<12} {couleur}{statut}{reset}")

    print(f"  {'─'*65}")
    return suspects

def menu():
    print("\n🔍  Process Monitor — Lemon Tools")
    print("=" * 45)
    print(f"  🕐 {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
    print("  [1] Scan rapide — Top 40 processus")
    print("  [2] Scan suspects uniquement")
    print("  [3] Chercher un processus par nom")
    print("  [0] Quitter")
    print(f"  {'─'*45}")
    return input("\n  👉 Choix : ").strip()

def main():
    choix = menu()

    if choix == "1":
        print("\n  ⏳ Analyse des processus en cours...")
        processus = get_processus()
        suspects = afficher_processus(processus)

        print(f"\n  📊 {len(processus)} processus analysés")
        if suspects:
            print(f"  \033[1;31m⚠️  {len(suspects)} processus suspect(s) détecté(s) !\033[0m")
            notifier(f"⚠️ {len(suspects)} processus suspect(s) détecté(s) !")
        else:
            print(f"  \033[1;32m✅ Aucun processus suspect détecté\033[0m")
            notifier("✅ Aucun processus suspect détecté")

    elif choix == "2":
        print("\n  ⏳ Recherche de processus suspects...")
        processus = get_processus()
        suspects = [p for p in processus if analyser_processus(p)[0] != "Normal"]

        if not suspects:
            print("\n  \033[1;32m✅ Aucun processus suspect détecté !\033[0m")
            notifier("✅ Mac sain — aucun suspect")
        else:
            print(f"\n  \033[1;31m⚠️  {len(suspects)} suspect(s) :\033[0m")
            afficher_processus(suspects)
            notifier(f"⚠️ {len(suspects)} processus suspect(s) !")

    elif choix == "3":
        nom = input("\n  🔍 Nom du processus à chercher : ").strip().lower()
        processus = get_processus()
        trouves = [p for p in processus if nom in p["nom"].lower() or nom in p["cmd"].lower()]

        if not trouves:
            print(f"\n  ❌ Aucun processus '{nom}' trouvé")
        else:
            print(f"\n  📊 {len(trouves)} résultat(s) pour '{nom}' :")
            afficher_processus(trouves)

    input("\n\n  ✅ Terminé — appuyez sur Entrée...")

if __name__ == "__main__":
    main()
