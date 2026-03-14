#!/usr/bin/env python3
"""
🎵 Spotify Controller — Lemon Tools
Contrôle Spotify depuis le terminal.
"""

import subprocess
import os
from datetime import datetime

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout.strip()
    except:
        return ""

def spotify(action):
    return run(f'osascript -e \'tell application "Spotify" to {action}\'')

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "🎵 Spotify"\'')

def get_info():
    try:
        state   = spotify("get player state")
        track   = spotify("get name of current track")
        artist  = spotify("get artist of current track")
        album   = spotify("get album of current track")
        dur_ms  = spotify("get duration of current track")
        pos_ms  = spotify("get player position")

        dur_s = int(dur_ms) // 1000 if dur_ms else 0
        pos_s = int(float(pos_ms)) if pos_ms else 0

        return {
            "state": state,
            "track": track,
            "artist": artist,
            "album": album,
            "duration": dur_s,
            "position": pos_s,
        }
    except:
        return None

def formater_temps(secondes):
    m = int(secondes // 60)
    s = int(secondes % 60)
    return f"{m}:{s:02d}"

def barre_progression(pos, total, largeur=25):
    if total == 0:
        return "░" * largeur
    pct = pos / total
    filled = int(largeur * pct)
    empty = largeur - filled
    return f"\033[1;32m{'█' * filled}\033[0;32m{'░' * empty}\033[0m"

def afficher_info(info):
    if not info:
        print("\n  ❌ Spotify n'est pas ouvert")
        print("  💡 Lance Spotify d'abord")
        return

    state_emoji = "▶️" if info["state"] == "playing" else "⏸️"
    state_txt = "En lecture" if info["state"] == "playing" else "En pause"

    print(f"\n  {state_emoji}  {state_txt}")
    print(f"  {'─'*42}")
    print(f"  🎵 {info['track']}")
    print(f"  👤 {info['artist']}")
    print(f"  💿 {info['album']}")

    barre = barre_progression(info["position"], info["duration"])
    pos_str = formater_temps(info["position"])
    dur_str = formater_temps(info["duration"])
    print(f"\n  {barre}  {pos_str} / {dur_str}")
    print(f"  {'─'*42}")

def menu():
    os.system("clear")
    print("\n\033[1;32m  🎵  Spotify Controller — Lemon Tools\033[0m")
    print(f"  \033[0;32m{'═' * 42}\033[0m\n")

    info = get_info()
    afficher_info(info)

    print(f"\n  [1] ▶️  Play / ⏸️  Pause")
    print(f"  [2] ⏭️  Suivant")
    print(f"  [3] ⏮️  Précédent")
    print(f"  [4] 🔊 Volume +")
    print(f"  [5] 🔉 Volume -")
    print(f"  [6] 🔀 Shuffle on/off")
    print(f"  [7] 🔁 Repeat on/off")
    print(f"  [8] 🔍 Rechercher une chanson")
    print(f"  [R] 🔄 Rafraîchir")
    print(f"  [0] Quitter")
    print(f"  \033[0;32m{'─' * 42}\033[0m")
    return input("\n  👉 Choix : ").strip()

def main():
    # Vérifier si Spotify est installé
    check = "true" if os.path.exists(os.path.expanduser("~/Applications/Spotify.app")) else "false"
    if check == "true":
        print("\n  ❌ Spotify n'est pas installé")
        input("  Appuyez sur Entrée...")
        return

    # Ouvrir Spotify si fermé
    run('open ~/Applications/Spotify.app')
    import time
    time.sleep(1)

    while True:
        choix = menu()

        if choix == "0":
            os.system("clear")
            break

        elif choix == "1":
            state = spotify("get player state")
            if state == "playing":
                spotify("pause")
                notifier("⏸️ Pause")
            else:
                spotify("play")
                info = get_info()
                if info:
                    notifier(f"▶️ {info['track']} — {info['artist']}")

        elif choix == "2":
            spotify("next track")
            import time; time.sleep(0.5)
            info = get_info()
            if info:
                notifier(f"⏭️ {info['track']} — {info['artist']}")

        elif choix == "3":
            spotify("previous track")
            import time; time.sleep(0.5)
            info = get_info()
            if info:
                notifier(f"⏮️ {info['track']} — {info['artist']}")

        elif choix == "4":
            vol = spotify("get sound volume")
            try:
                new_vol = min(100, int(vol) + 10)
                spotify(f"set sound volume to {new_vol}")
                print(f"\n  🔊 Volume : {new_vol}%")
            except:
                pass

        elif choix == "5":
            vol = spotify("get sound volume")
            try:
                new_vol = max(0, int(vol) - 10)
                spotify(f"set sound volume to {new_vol}")
                print(f"\n  🔉 Volume : {new_vol}%")
            except:
                pass

        elif choix == "6":
            shuffle = spotify("get shuffling")
            new_shuffle = "false" if shuffle == "true" else "true"
            spotify(f"set shuffling to {new_shuffle}")
            state = "🔀 ON" if new_shuffle == "true" else "🔀 OFF"
            print(f"\n  Shuffle : {state}")
            notifier(f"Shuffle {state}")

        elif choix == "7":
            repeat = spotify("get repeating")
            new_repeat = "false" if repeat == "true" else "true"
            spotify(f"set repeating to {new_repeat}")
            state = "🔁 ON" if new_repeat == "true" else "🔁 OFF"
            print(f"\n  Repeat : {state}")
            notifier(f"Repeat {state}")

        elif choix == "8":
            query = input("\n  🔍 Rechercher : ").strip()
            if query:
                run(f'osascript -e \'tell application "Spotify" to search for "{query}"\'')
                print(f"  ✅ Recherche lancée dans Spotify !")

        elif choix.upper() == "R":
            continue

        if choix not in ["0", "R", "r"]:
            import time; time.sleep(0.3)

if __name__ == "__main__":
    main()
