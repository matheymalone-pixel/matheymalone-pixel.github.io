#!/usr/bin/env python3
"""
🌤️ Météo — Lemon Tools
Détecte ta position GPS via IP et affiche la météo locale précise.
"""

import subprocess
import json
from datetime import datetime

def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "🌤️ Météo"\'')

def meteo():
    print("\n🌤️  Météo — Lemon Tools")
    print("=" * 45)
    print("  ⏳ Récupération de ta position...\n")

    # Détection coordonnées GPS précises via IP
    geo = run("curl -s ipinfo.io 2>/dev/null")
    try:
        geo_data = json.loads(geo)
        coords = geo_data.get("loc", "14.6037,-61.0624")
        ville_nom_ip = geo_data.get("city", "")
        pays_ip = geo_data.get("country", "")
    except:
        coords = "14.6037,-61.0624"
        ville_nom_ip = ""
        pays_ip = ""

    lat, lon = coords.split(",")

    # Récupération météo via coordonnées GPS
    data = run(f"curl -s 'wttr.in/{lat},{lon}?format=j1' 2>/dev/null")

    if not data:
        print("  ❌ Impossible de récupérer la météo")
        print("  💡 Vérifiez votre connexion internet")
        return

    try:
        w = json.loads(data)
        current = w["current_condition"][0]
        area = w["nearest_area"][0]

        ville_affich = ville_nom_ip if ville_nom_ip else area["areaName"][0]["value"]
        pays_affich = pays_ip if pays_ip else area["country"][0]["value"]
        temp = current["temp_C"]
        ressenti = current["FeelsLikeC"]
        humidite = current["humidity"]
        vent = current["windspeedKmph"]
        desc = current["weatherDesc"][0]["value"]
        visibilite = current["visibility"]
        pression = current["pressure"]
        uv = current["uvIndex"]

        # Traduction descriptions
        traductions = {
            "sunny": "Ensoleillé", "clear": "Ciel dégagé",
            "partly cloudy": "Partiellement nuageux", "cloudy": "Nuageux",
            "overcast": "Couvert", "light rain": "Pluie légère",
            "patchy rain nearby": "Pluie proche", "moderate rain": "Pluie modérée",
            "heavy rain": "Forte pluie", "light rain shower": "Averse légère",
            "thundery outbreaks": "Orages", "fog": "Brouillard",
            "mist": "Brume", "blizzard": "Blizzard", "snow": "Neige",
        }
        desc_fr = traductions.get(desc.lower(), desc)

        # Emoji météo
        desc_lower = desc.lower()
        if "sunny" in desc_lower or "clear" in desc_lower:
            emoji = "☀️"
        elif "thunder" in desc_lower or "storm" in desc_lower:
            emoji = "⛈️"
        elif "rain" in desc_lower or "drizzle" in desc_lower or "shower" in desc_lower:
            emoji = "🌧️"
        elif "snow" in desc_lower or "blizzard" in desc_lower:
            emoji = "❄️"
        elif "fog" in desc_lower or "mist" in desc_lower:
            emoji = "🌫️"
        elif "overcast" in desc_lower:
            emoji = "🌥️"
        elif "cloud" in desc_lower:
            emoji = "⛅"
        else:
            emoji = "🌤️"

        # Couleur température
        t = int(temp)
        if t <= 0:    c = "\033[1;34m"
        elif t <= 10: c = "\033[1;36m"
        elif t <= 20: c = "\033[1;32m"
        elif t <= 30: c = "\033[1;33m"
        else:         c = "\033[1;31m"
        r = "\033[0m"

        print(f"  📍 {ville_affich}, {pays_affich}  ({lat}, {lon})")
        print(f"  🕐 {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        print(f"\n  {'─'*40}")
        print(f"  {emoji}  Ciel        : {desc_fr}")
        print(f"  🌡️  Température : {c}{temp}°C{r}")
        print(f"  🤔  Ressenti    : {ressenti}°C")
        print(f"  💧  Humidité    : {humidite}%")
        print(f"  🌬️  Vent        : {vent} km/h")
        print(f"  👁️  Visibilité  : {visibilite} km")
        print(f"  📊  Pression    : {pression} hPa")
        print(f"  ☀️  Index UV    : {uv}")
        print(f"  {'─'*40}\n")

        # Prévisions 3 jours
        print("  📅 Prévisions 3 jours")
        print(f"  {'─'*40}")
        jours = ["Aujourd'hui  ", "Demain       ", "Après-demain "]
        for i, jour_data in enumerate(w["weather"][:3]):
            max_t = jour_data["maxtempC"]
            min_t = jour_data["mintempC"]
            desc_j = jour_data["hourly"][4]["weatherDesc"][0]["value"]
            desc_j_fr = traductions.get(desc_j.lower(), desc_j)
            print(f"  {jours[i]}  {min_t}°C → {max_t}°C   {desc_j_fr}")

        print(f"  {'─'*40}\n")

        notifier(f"{emoji} {ville_affich} — {temp}°C — {desc_fr}")

    except Exception as e:
        print(f"  ❌ Erreur : {e}")

if __name__ == "__main__":
    meteo()
