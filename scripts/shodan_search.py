#!/usr/bin/env python3
"""
📡 Shodan Search — Lemon Tools
Trouve des appareils exposés sur internet.
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
    run(f'osascript -e \'display notification "{message}" with title "📡 Shodan"\'')

def get_api_key():
    key = run('security find-generic-password -s "shodan-api" -a "lemon" -w 2>/dev/null')
    return key if key else None

def shodan_search(query, api_key, page=1):
    url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query.replace(' ', '+')}&page={page}"
    data = run(f'curl -s --max-time 15 "{url}"')
    try:
        return json.loads(data)
    except:
        return None

def shodan_host(ip, api_key):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
    data = run(f'curl -s --max-time 15 "{url}"')
    try:
        return json.loads(data)
    except:
        return None

def shodan_info(api_key):
    url = f"https://api.shodan.io/api-info?key={api_key}"
    data = run(f'curl -s --max-time 10 "{url}"')
    try:
        return json.loads(data)
    except:
        return None

def afficher_resultat(match):
    reset = "\033[0m"
    ip       = match.get("ip_str", "?")
    port     = match.get("port", "?")
    org      = match.get("org", "Inconnu")
    pays     = match.get("location", {}).get("country_name", "?")
    ville    = match.get("location", {}).get("city", "")
    hostnames = match.get("hostnames", [])
    vulns    = match.get("vulns", {})
    banner   = match.get("data", "")[:100]

    print(f"\n  \033[1;36m{'─'*50}\033[0m")
    print(f"  🌐 IP      : \033[1;37m{ip}\033[0m  Port: \033[1;33m{port}\033[0m")
    print(f"  🏢 Org     : {org}")
    print(f"  📍 Lieu    : {ville}, {pays}")

    if hostnames:
        print(f"  🔗 Host    : {', '.join(hostnames[:2])}")

    if vulns:
        print(f"  \033[1;31m⚠️  Vulnérabilités : {', '.join(list(vulns.keys())[:3])}\033[0m")

    if banner:
        print(f"  📋 Banner  : \033[0;35m{banner[:80]}\033[0m")

def afficher_host(data):
    if not data or "error" in data:
        print(f"\n  ❌ {data.get('error', 'Erreur inconnue')}")
        return

    ip       = data.get("ip_str", "?")
    org      = data.get("org", "?")
    pays     = data.get("country_name", "?")
    ville    = data.get("city", "")
    hostnames = data.get("hostnames", [])
    ports    = data.get("ports", [])
    vulns    = data.get("vulns", {})
    os_info  = data.get("os", "")
    tags     = data.get("tags", [])
    derniere_maj = data.get("last_update", "?")

    print(f"\n  \033[1;36m{'═'*50}\033[0m")
    print(f"  🌐 IP          : \033[1;37m{ip}\033[0m")
    print(f"  🏢 Organisation: {org}")
    print(f"  📍 Localisation: {ville}, {pays}")

    if hostnames:
        print(f"  🔗 Hostnames   : {', '.join(hostnames[:3])}")

    if os_info:
        print(f"  💻 OS          : {os_info}")

    if ports:
        ports_str = ", ".join([str(p) for p in ports[:10]])
        print(f"  🚪 Ports       : \033[1;33m{ports_str}\033[0m")

    if tags:
        print(f"  🏷️  Tags        : {', '.join(tags)}")

    if vulns:
        print(f"\n  \033[1;31m⚠️  {len(vulns)} vulnérabilité(s) :\033[0m")
        for cve, info in list(vulns.items())[:5]:
            cvss = info.get("cvss", "?")
            print(f"  \033[1;31m  • {cve}\033[0m  CVSS: {cvss}")

    print(f"\n  🕐 Dernière MAJ: {derniere_maj}")
    print(f"  \033[1;36m{'═'*50}\033[0m")

def recherches_rapides():
    print("\n  🚀 Recherches rapides :")
    print(f"  {'─'*40}")
    recherches = [
        ("1", "Webcams France",          "webcam country:FR"),
        ("2", "Routeurs Martinique",      "country:MQ port:80"),
        ("3", "Serveurs SSH exposés",     "port:22 product:OpenSSH"),
        ("4", "Bases de données MongoDB", "product:MongoDB port:27017"),
        ("5", "Caméras IP Hikvision",     "product:Hikvision"),
        ("6", "Imprimantes exposées",     "port:9100 product:printer"),
        ("7", "Raspberry Pi",             "product:Raspbian"),
        ("8", "Serveurs FTP anonymes",    "port:21 Anonymous"),
    ]
    for num, label, _ in recherches:
        print(f"  [{num}] {label}")
    print(f"  {'─'*40}")
    choix = input("\n  👉 Choix : ").strip()
    for num, _, query in recherches:
        if choix == num:
            return query
    return None

def menu():
    os.system("clear")
    print("\n\033[1;31m  📡  Shodan Search — Lemon Tools\033[0m")
    print(f"  \033[0;31m{'═' * 42}\033[0m\n")
    print("  ⚠️  Usage éthique uniquement — ne pas abuser\n")
    print("  [1] Recherche personnalisée")
    print("  [2] Recherches rapides")
    print("  [3] Analyser une IP")
    print("  [4] Mon compte Shodan")
    print("  [0] Quitter")
    print(f"  \033[0;31m{'─' * 42}\033[0m")
    return input("\n  👉 Choix : ").strip()

def main():
    api_key = get_api_key()
    if not api_key:
        print("\n  ❌ Clé API Shodan non trouvée")
        print("  💡 Lance : security add-generic-password -s 'shodan-api' -a 'lemon' -w 'TA_CLE'")
        input("\n  Appuyez sur Entrée...")
        return

    while True:
        choix = menu()

        if choix == "0":
            os.system("clear")
            break

        elif choix == "1":
            query = input("\n  🔍 Recherche Shodan : ").strip()
            if not query:
                continue
            print(f"\n  ⏳ Recherche : {query}...")
            data = shodan_search(query, api_key)
            if not data or "error" in data:
                print(f"\n  ❌ {data.get('error', 'Erreur') if data else 'Pas de résultat'}")
            else:
                total = data.get("total", 0)
                matches = data.get("matches", [])
                print(f"\n  📊 {total} résultat(s) — affichage des {len(matches)} premiers")
                for m in matches[:5]:
                    afficher_resultat(m)
                notifier(f"📡 {total} résultats pour '{query}'")

        elif choix == "2":
            query = recherches_rapides()
            if query:
                print(f"\n  ⏳ Recherche : {query}...")
                data = shodan_search(query, api_key)
                if not data or "error" in data:
                    print(f"\n  ❌ {data.get('error', 'Erreur') if data else 'Pas de résultat'}")
                else:
                    total = data.get("total", 0)
                    matches = data.get("matches", [])
                    print(f"\n  📊 {total} résultat(s)")
                    for m in matches[:5]:
                        afficher_resultat(m)
                    notifier(f"📡 {total} résultats trouvés")

        elif choix == "3":
            ip = input("\n  🌐 IP à analyser : ").strip()
            if ip:
                print(f"\n  ⏳ Analyse de {ip}...")
                data = shodan_host(ip, api_key)
                afficher_host(data)
                notifier(f"📡 Analyse {ip} terminée")

        elif choix == "4":
            data = shodan_info(api_key)
            if data:
                print(f"\n  👤 Compte Shodan")
                print(f"  {'─'*40}")
                print(f"  Plan     : {data.get('plan', '?')}")
                print(f"  Crédits  : {data.get('query_credits', '?')} requêtes restantes")
                print(f"  Scan     : {data.get('scan_credits', '?')} scans restants")

        input("\n\n  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
