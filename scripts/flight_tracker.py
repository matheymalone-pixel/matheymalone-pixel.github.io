#!/usr/bin/env python3
"""
✈️ Flight Tracker — Lemon Tools
Suit les vols en temps réel via OpenSky Network.
"""

import subprocess
import json
import os
from datetime import datetime

def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "✈️ Flight Tracker"\'')

def get_vols_zone(lamin, lomin, lamax, lomax):
    url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
    data = run(f'curl -s --max-time 10 "{url}"')
    try:
        return json.loads(data)
    except:
        return None

def get_vol_callsign(callsign):
    url = f"https://opensky-network.org/api/states/all"
    data = run(f'curl -s --max-time 10 "{url}"')
    try:
        result = json.loads(data)
        if result and result.get("states"):
            for state in result["states"]:
                if state[1] and callsign.upper() in state[1].upper():
                    return state
    except:
        pass
    return None

def formater_vol(state):
    if not state:
        return None
    callsign   = state[1].strip() if state[1] else "?"
    origine    = state[2] if state[2] else "?"
    altitude   = round(state[7]) if state[7] else 0
    vitesse    = round(state[9] * 3.6) if state[9] else 0
    cap        = round(state[10]) if state[10] else 0
    lat        = round(state[6], 4) if state[6] else 0
    lon        = round(state[5], 4) if state[5] else 0
    au_sol     = state[8] if state[8] is not None else False

    return {
        "callsign": callsign,
        "origine": origine,
        "altitude": altitude,
        "vitesse": vitesse,
        "cap": cap,
        "lat": lat,
        "lon": lon,
        "au_sol": au_sol,
    }

def afficher_vol(vol):
    if not vol:
        return
    reset = "\033[0m"
    statut = "🛬 Au sol" if vol["au_sol"] else "✈️  En vol"

    print(f"\n  \033[1;36m{'─'*45}\033[0m")
    print(f"  ✈️  \033[1;37m{vol['callsign']}\033[0m  —  {statut}")
    print(f"  \033[1;36m{'─'*45}\033[0m")
    print(f"  🌍 Pays d'origine : {vol['origine']}")
    print(f"  📍 Position       : {vol['lat']}°N, {vol['lon']}°E")
    print(f"  🏔️  Altitude       : \033[1;33m{vol['altitude']} m\033[0m ({round(vol['altitude']*3.28084)} ft)")
    print(f"  💨 Vitesse        : \033[1;32m{vol['vitesse']} km/h\033[0m")
    print(f"  🧭 Cap            : {vol['cap']}°")
    print(f"  \033[1;36m{'─'*45}\033[0m\n")

def vols_martinique():
    print("\n  ⏳ Recherche des vols autour de la Martinique...")
    # Zone Martinique élargie
    data = get_vols_zone(13.5, -62, 15.5, -59.5)

    if not data or not data.get("states"):
        print("\n  📭 Aucun vol détecté autour de la Martinique")
        print("  💡 Essaie dans quelques minutes")
        return

    vols = [formater_vol(s) for s in data["states"] if s]
    vols = [v for v in vols if v]

    print(f"\n  ✈️  {len(vols)} vol(s) détecté(s) autour de la Martinique")
    print(f"  🕐 {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
    print(f"\n  {'CALLSIGN':<12} {'ALTITUDE':<12} {'VITESSE':<12} {'CAP':<8} STATUT")
    print(f"  {'─'*55}")

    for v in vols:
        statut = "🛬 Sol" if v["au_sol"] else "✈️  Vol"
        print(f"  {v['callsign']:<12} {str(v['altitude'])+'m':<12} {str(v['vitesse'])+'km/h':<12} {str(v['cap'])+'°':<8} {statut}")

    notifier(f"✈️ {len(vols)} vol(s) autour de la Martinique")

def chercher_vol():
    callsign = input("\n  ✈️  Numéro de vol (ex: AF456, BW301) : ").strip()
    if not callsign:
        return

    print(f"\n  ⏳ Recherche du vol {callsign}...")
    state = get_vol_callsign(callsign)

    if not state:
        print(f"\n  ❌ Vol {callsign} non trouvé")
        print("  💡 Vérifiez le numéro ou réessayez dans quelques minutes")
        return

    vol = formater_vol(state)
    afficher_vol(vol)
    notifier(f"✈️ {vol['callsign']} — {vol['altitude']}m — {vol['vitesse']}km/h")

def vols_zone_custom():
    print("\n  🌍 Recherche par zone géographique")
    print("  💡 Exemple Martinique : 13.5 / -62 / 15.5 / -59.5")
    print(f"  {'─'*40}")
    try:
        lamin = float(input("  Latitude min  : ").strip())
        lomin = float(input("  Longitude min : ").strip())
        lamax = float(input("  Latitude max  : ").strip())
        lomax = float(input("  Longitude max : ").strip())
    except:
        print("  ❌ Valeurs invalides")
        return

    print(f"\n  ⏳ Scan de la zone...")
    data = get_vols_zone(lamin, lomin, lamax, lomax)

    if not data or not data.get("states"):
        print("\n  📭 Aucun vol dans cette zone")
        return

    vols = [formater_vol(s) for s in data["states"] if s]
    vols = [v for v in vols if v]

    print(f"\n  ✈️  {len(vols)} vol(s) détecté(s)")
    for v in vols:
        afficher_vol(v)

def menu():
    os.system("clear")
    print("\n\033[1;36m  ✈️   Flight Tracker — Lemon Tools\033[0m")
    print(f"  \033[0;36m{'═' * 42}\033[0m\n")
    print("  [1] Vols autour de la Martinique")
    print("  [2] Chercher un vol par numéro")
    print("  [3] Scanner une zone personnalisée")
    print("  [0] Quitter")
    print(f"  \033[0;36m{'─' * 42}\033[0m")
    return input("\n  👉 Choix : ").strip()

def main():
    while True:
        choix = menu()
        if choix == "0":
            os.system("clear")
            break
        elif choix == "1":
            vols_martinique()
        elif choix == "2":
            chercher_vol()
        elif choix == "3":
            vols_zone_custom()
        input("\n  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
