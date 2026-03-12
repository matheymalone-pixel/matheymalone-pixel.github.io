#!/usr/bin/env python3
"""
⏱️ Pomodoro Timer — Lemon Tools
Timer 25min travail / 5min pause.
"""

import time
import os
import subprocess
from datetime import datetime

def run(cmd):
    try:
        subprocess.run(cmd, shell=True, capture_output=True)
    except:
        pass

def notifier(titre, message, son=True):
    run(f'osascript -e \'display notification "{message}" with title "{titre}" sound name "Glass"\'')

def barre_progression(elapsed, total, largeur=30):
    pct = elapsed / total
    filled = int(largeur * pct)
    empty = largeur - filled
    return f"\033[1;35m{'█' * filled}\033[0;35m{'░' * empty}\033[0m"

def formater_temps(secondes):
    m = int(secondes // 60)
    s = int(secondes % 60)
    return f"{m:02d}:{s:02d}"

def timer(duree_sec, label, emoji, couleur):
    os.system("clear")
    debut = time.time()

    while True:
        elapsed = time.time() - debut
        restant = duree_sec - elapsed

        if restant <= 0:
            break

        pct = int(elapsed / duree_sec * 100)
        barre = barre_progression(elapsed, duree_sec)

        os.system("clear")
        print(f"\n{couleur}  {emoji}  {label}\033[0m")
        print(f"  \033[0;35m{'═' * 40}\033[0m")
        print(f"\n  ⏰  Temps restant : \033[1;37m{formater_temps(restant)}\033[0m")
        print(f"\n  {barre}  {pct}%")
        print(f"\n  🕐 Démarré à {datetime.now().strftime('%H:%M')}")
        print(f"\n  \033[0;35m{'─' * 40}\033[0m")
        print(f"  [Q] Abandonner")

        # Check input non-bloquant
        import select, sys
        r, _, _ = select.select([sys.stdin], [], [], 1)
        if r:
            c = sys.stdin.readline().strip().upper()
            if c == "Q":
                return False

    return True

def afficher_stats(sessions, pauses):
    print(f"\n  📊 Session actuelle")
    print(f"  {'─'*35}")
    print(f"  🍅 Pomodoros terminés : \033[1;32m{sessions}\033[0m")
    print(f"  ☕ Pauses prises      : \033[1;32m{pauses}\033[0m")
    print(f"  ⏱️  Temps de travail   : \033[1;32m{sessions * 25} min\033[0m")

def menu():
    os.system("clear")
    print("\n\033[1;35m  ⏱️   Pomodoro Timer — Lemon Tools\033[0m")
    print(f"  \033[0;35m{'═' * 40}\033[0m\n")
    print("  [1] Démarrer Pomodoro    25 min 🍅")
    print("  [2] Pause courte          5 min ☕")
    print("  [3] Pause longue         15 min 🌴")
    print("  [4] Session complète     4x Pomodoro")
    print("  [0] Quitter")
    print(f"  \033[0;35m{'─' * 40}\033[0m")
    return input("\n  👉 Choix : ").strip()

def session_complete():
    sessions = 0
    pauses = 0
    os.system("clear")
    print("\n\033[1;35m  🍅 Session complète — 4 Pomodoros\033[0m")
    print(f"  \033[0;35m{'═' * 40}\033[0m")
    print("  4x (25min travail + 5min pause)")
    print("  + 1 pause longue de 15min à la fin")
    print(f"  Durée totale : ~2h\033[0m")
    input("\n  Appuyez sur Entrée pour démarrer...")

    for i in range(1, 5):
        print(f"\n  🍅 Pomodoro {i}/4")
        ok = timer(25 * 60, f"Pomodoro {i}/4 — Travail !", "🍅", "\033[1;31m")
        if not ok:
            break
        sessions += 1
        notifier("🍅 Pomodoro terminé !", f"Pomodoro {i}/4 terminé — Pause !")

        if i < 4:
            input(f"\n  ☕ Pomodoro {i} terminé ! Appuyez sur Entrée pour la pause...")
            timer(5 * 60, "Pause courte — Repose-toi !", "☕", "\033[1;36m")
            pauses += 1
            notifier("☕ Pause terminée !", "Retour au travail !")

    notifier("🌴 Session complète !", "Prends une vraie pause de 15 min !")
    timer(15 * 60, "Pause longue — Tu l'as mérité !", "🌴", "\033[1;32m")
    afficher_stats(sessions, pauses)

def main():
    sessions = 0
    pauses = 0

    while True:
        choix = menu()

        if choix == "0":
            os.system("clear")
            break

        elif choix == "1":
            input("\n  🍅 Prêt ? Appuyez sur Entrée pour démarrer...")
            ok = timer(25 * 60, "Pomodoro — Concentration !", "🍅", "\033[1;31m")
            if ok:
                sessions += 1
                notifier("🍅 Pomodoro terminé !", "25 minutes écoulées — Prends une pause !")
                print(f"\n  \033[1;32m✅ Pomodoro terminé !\033[0m")
            afficher_stats(sessions, pauses)
            input("\n  Appuyez sur Entrée pour continuer...")

        elif choix == "2":
            input("\n  ☕ Pause de 5 min. Appuyez sur Entrée...")
            ok = timer(5 * 60, "Pause courte — Repose-toi !", "☕", "\033[1;36m")
            if ok:
                pauses += 1
                notifier("☕ Pause terminée !", "Retour au travail !")
            afficher_stats(sessions, pauses)
            input("\n  Appuyez sur Entrée pour continuer...")

        elif choix == "3":
            input("\n  🌴 Pause de 15 min. Appuyez sur Entrée...")
            ok = timer(15 * 60, "Pause longue — Tu l'as mérité !", "🌴", "\033[1;32m")
            if ok:
                pauses += 1
                notifier("🌴 Pause longue terminée !", "Retour au travail !")
            afficher_stats(sessions, pauses)
            input("\n  Appuyez sur Entrée pour continuer...")

        elif choix == "4":
            session_complete()
            input("\n  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
