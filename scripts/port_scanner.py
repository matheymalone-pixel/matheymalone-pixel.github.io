#!/usr/bin/env python3
"""
📡 Port Scanner Avancé — Lemon Tools
Scan réseau plus poussé que netaudit.
"""

import subprocess
import socket
import json
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "📡 Port Scanner"\'')

PORTS_CONNUS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5900: "VNC", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    27017: "MongoDB", 6379: "Redis", 5432: "PostgreSQL",
}

PORTS_DANGEREUX = [21, 23, 445, 3389, 5900, 27017, 6379]

def get_ip_locale():
    result = run("ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null")
    return result if result else "192.168.1.1"

def get_passerelle():
    result = run("route -n get default 2>/dev/null | grep gateway | awk '{print $2}'")
    return result if result else ""

def get_subnet():
    ip = get_ip_locale()
    parts = ip.split(".")
    return f"{parts[0]}.{parts[1]}.{parts[2]}"

def scanner_port(ip, port, timeout=0.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return port if result == 0 else None
    except:
        return None

def scanner_ports_host(ip, ports, timeout=0.5):
    ouverts = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scanner_port, ip, p, timeout): p for p in ports}
        for future in as_completed(futures):
            result = future.result()
            if result:
                ouverts.append(result)
    return sorted(ouverts)

def scanner_reseau():
    subnet = get_subnet()
    print(f"\n  🔍 Scan du réseau {subnet}.0/24...")
    print(f"  {'─'*45}")

    actifs = []
    def ping(i):
        ip = f"{subnet}.{i}"
        result = run(f"ping -c 1 -W 1 {ip} 2>/dev/null | grep '1 packets transmitted'")
        return ip if result else None

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(ping, i) for i in range(1, 255)]
        for future in as_completed(futures):
            ip = future.result()
            if ip:
                actifs.append(ip)

    return sorted(actifs, key=lambda x: int(x.split(".")[-1]))

def scanner_approfondi(ip):
    ports_communs = list(PORTS_CONNUS.keys())
    print(f"\n  🔍 Scan approfondi de {ip}...")
    ouverts = scanner_ports_host(ip, ports_communs)

    if not ouverts:
        print(f"  ✅ Aucun port ouvert détecté")
        return []

    dangers = []
    for port in ouverts:
        service = PORTS_CONNUS.get(port, "Inconnu")
        if port in PORTS_DANGEREUX:
            print(f"  \033[1;31m⚠️  Port {port:<6} {service:<15} — DANGEREUX\033[0m")
            dangers.append(port)
        else:
            print(f"  \033[1;32m✅  Port {port:<6} {service}\033[0m")

    return dangers

def menu():
    print("\n📡  Port Scanner Avancé — Lemon Tools")
    print("=" * 45)
    print(f"  🕐 {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    ip_locale = get_ip_locale()
    passerelle = get_passerelle()
    print(f"  💻 Ton IP    : \033[1;36m{ip_locale}\033[0m")
    print(f"  🌐 Passerelle: \033[1;36m{passerelle}\033[0m")
    print(f"\n  [1] Scanner tous les ports de ton Mac")
    print(f"  [2] Scanner un appareil du réseau")
    print(f"  [3] Découvrir les appareils actifs")
    print(f"  [4] Scan complet réseau + ports dangereux")
    print(f"  [0] Quitter")
    print(f"  {'─'*45}")
    return input("\n  👉 Choix : ").strip()

def main():
    choix = menu()

    if choix == "1":
        ip = get_ip_locale()
        dangers = scanner_approfondi(ip)
        if dangers:
            notifier(f"⚠️ {len(dangers)} port(s) dangereux sur ton Mac !")
        else:
            notifier("✅ Aucun port dangereux sur ton Mac")

    elif choix == "2":
        ip = input("\n  🎯 IP à scanner (ex: 192.168.1.10) : ").strip()
        if ip:
            scanner_approfondi(ip)

    elif choix == "3":
        actifs = scanner_reseau()
        print(f"\n  📊 {len(actifs)} appareil(s) actif(s) :")
        passerelle = get_passerelle()
        for ip in actifs:
            label = " ← Passerelle" if ip == passerelle else ""
            label = " ← Ton Mac" if ip == get_ip_locale() else label
            print(f"  \033[1;36m•\033[0m {ip}{label}")
        notifier(f"📡 {len(actifs)} appareils actifs sur le réseau")

    elif choix == "4":
        print("\n  ⚠️  Scan complet en cours — cela peut prendre quelques minutes...")
        actifs = scanner_reseau()
        total_dangers = []
        for ip in actifs:
            dangers = scanner_approfondi(ip)
            total_dangers.extend(dangers)
        print(f"\n  {'─'*45}")
        print(f"  📊 {len(actifs)} appareils scannés")
        if total_dangers:
            print(f"  \033[1;31m⚠️  {len(total_dangers)} port(s) dangereux détectés !\033[0m")
            notifier(f"⚠️ {len(total_dangers)} ports dangereux sur le réseau !")
        else:
            print(f"  \033[1;32m✅ Aucun port dangereux détecté\033[0m")
            notifier("✅ Réseau sain — aucun port dangereux")

    input("\n\n  ✅ Terminé — appuyez sur Entrée...")

if __name__ == "__main__":
    main()
