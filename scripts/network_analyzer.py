#!/usr/bin/env python3
"""
🌐 Network Analyzer — Mac
Analyse complète de votre réseau WiFi.
Auteur : Malone | Usage : python3 network_analyzer.py
"""

import subprocess
import socket
import struct
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

RAPPORT_SORTIE = Path.home() / "Desktop" / f"network_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

PORTS_COMMUNS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet ⚠️",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    443:  "HTTPS",
    445:  "SMB ⚠️",
    3306: "MySQL",
    3389: "RDP ⚠️",
    5900: "VNC ⚠️",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017:"MongoDB",
}

resultats = {"safe": [], "warning": [], "danger": []}

EMAIL = "matheymalone@gmail.com"

# ─────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────

def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""

def titre(texte, emoji="🔍"):
    print(f"\n{'═'*55}")
    print(f"  {emoji} {texte}")
    print(f"{'═'*55}")

def log(niveau, categorie, message):
    icone = {"safe": "✅", "warning": "⚠️ ", "danger": "🚨"}[niveau]
    print(f"  {icone} [{categorie}] {message}")
    resultats[niveau].append(f"{icone} [{categorie}] {message}")

def notifier(titre_notif, message):
    """Notification Mac native."""
    run(f'osascript -e \'display notification "{message}" with title "{titre_notif}"\'')

# ─────────────────────────────────────────
# MODULE EMAIL
# ─────────────────────────────────────────

def get_password():
    """Récupère le mot de passe depuis le trousseau Mac."""
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "Lemon-scripts", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def envoyer_email(sujet, corps):
    """Envoie un email via Gmail."""
    try:
        password = get_password()
        msg = MIMEMultipart("alternative")
        msg["Subject"] = sujet
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg.attach(MIMEText(corps, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
            serveur.login(EMAIL, password)
            serveur.sendmail(EMAIL, EMAIL, msg.as_string())
        print("  📧 Email envoyé ✓")
    except Exception as e:
        print(f"  ❌ Erreur email : {e}")

def notifier_appareil_inconnu(ip, mac, hostname):
    """Alerte immédiate si appareil inconnu détecté."""
    sujet = f"🚨 Appareil inconnu sur ton réseau — {ip}"
    corps = f"""
🚨 ALERTE RÉSEAU — Malone Tools

Un appareil inconnu a été détecté sur ton réseau !

📍 IP       : {ip}
📟 MAC      : {mac}
🖥️  Hostname : {hostname}
🕐 Heure    : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}

Vérifie si tu reconnais cet appareil.
— Malone Tools
    """
    envoyer_email(sujet, corps)

def envoyer_rapport_complet():
    """Envoie le rapport complet par email."""
    nb_danger  = len(resultats["danger"])
    nb_warning = len(resultats["warning"])
    nb_safe    = len(resultats["safe"])

    if nb_danger == 0 and nb_warning <= 3:
        verdict = "🟢 Réseau sain"
    elif nb_danger == 0:
        verdict = "🟡 Quelques points à vérifier"
    else:
        verdict = "🔴 Éléments critiques !"

    sujet = f"📊 Rapport réseau — {verdict} — {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    corps = f"""
📊 RAPPORT RÉSEAU — Malone Tools
{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}

Verdict : {verdict}

🚨 Dangers      : {nb_danger}
⚠️  Avertissem. : {nb_warning}
✅ Safe         : {nb_safe}

{'─'*40}
DÉTAILS
{'─'*40}
"""
    for niveau in ["danger", "warning", "safe"]:
        if resultats[niveau]:
            label = {"danger": "🚨 DANGERS", "warning": "⚠️ AVERTISSEMENTS", "safe": "✅ SAFE"}[niveau]
            corps += f"\n{label}\n"
            for ligne in resultats[niveau]:
                corps += f"  {ligne}\n"

    corps += "\n— Malone Tools"
    envoyer_email(sujet, corps)

# ─────────────────────────────────────────
# DÉTECTION AUTOMATIQUE DE L'INTERFACE
# ─────────────────────────────────────────

def detecter_interface_active():
    """Trouve automatiquement l'interface réseau active."""
    route = run("route -n get default 2>/dev/null | grep interface | awk '{print $2}'")
    if route:
        return route.strip()
    for iface in ["en0", "en1", "en2", "utun0", "utun1"]:
        ip_test = run(f"ifconfig {iface} 2>/dev/null | grep 'inet ' | awk '{{print $2}}'")
        if ip_test and not ip_test.startswith("127."):
            return iface
    return "en0"

def obtenir_ssid(interface):
    """Récupère le nom du réseau WiFi ou le type de connexion."""
    ssid = run(f"/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I 2>/dev/null | grep ' SSID' | awk '{{print $2}}'")
    if ssid:
        return f"📶 {ssid} (WiFi)"
    if "utun" in interface or interface in ["en1", "en2"]:
        return "📱 Partage iPhone / Hotspot"
    if interface == "en0":
        link = run("ifconfig en0 | grep 'status:'")
        if "active" in link:
            return "🔌 Ethernet"
    return f"🌐 {interface}"

def obtenir_ip_locale(interface):
    """Récupère l'IP locale et le masque réseau sur l'interface donnée."""
    output = run(f"ifconfig {interface} | grep 'inet '")
    match = re.search(r"inet (\d+\.\d+\.\d+\.\d+) netmask (0x[0-9a-f]+)", output)
    if match:
        ip = match.group(1)
        masque_hex = int(match.group(2), 16)
        masque = socket.inet_ntoa(struct.pack(">I", masque_hex))
        ip_parts = list(map(int, ip.split(".")))
        masque_parts = list(map(int, masque.split(".")))
        reseau = ".".join(str(i & m) for i, m in zip(ip_parts, masque_parts))
        return ip, masque, reseau
    return None, None, None

# ─────────────────────────────────────────
# 1. INFOS RÉSEAU
# ─────────────────────────────────────────

def infos_reseau():
    titre("Informations réseau", "📡")

    interface = detecter_interface_active()
    ssid = obtenir_ssid(interface)
    ip, masque, reseau = obtenir_ip_locale(interface)
    gateway = run("netstat -nr | grep default | head -1 | awk '{print $2}'")
    dns = run("scutil --dns | grep 'nameserver\\[0\\]' | head -3 | awk '{print $3}'")
    mac_addr = run(f"ifconfig {interface} | grep ether | awk '{{print $2}}'")

    print(f"""
  🔌 Interface    : {interface}
  📶 Réseau       : {ssid}
  🖥️  Votre IP     : {ip}
  🔀 Masque       : {masque}
  🌐 Plage réseau : {reseau}/24
  🚪 Passerelle   : {gateway}
  🔤 DNS          : {dns.replace(chr(10), ', ')}
  📟 Adresse MAC  : {mac_addr}
    """)

    if dns:
        for d in dns.split("\n"):
            d = d.strip()
            if not d:
                continue
            if d in ["8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "9.9.9.9"]:
                log("safe", "DNS", f"{d} → DNS public connu ✓")
            elif re.match(r"^(192\.168\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|172\.20\.)", d):
                log("safe", "DNS", f"{d} → DNS de votre routeur (normal) ✓")
            else:
                log("warning", "DNS", f"{d} → DNS non standard, vérifiez !")

    return ip, reseau, gateway, interface

# ─────────────────────────────────────────
# 2. APPAREILS SUR LE RÉSEAU
# ─────────────────────────────────────────

def scanner_appareils(reseau, mon_ip):
    titre("Appareils connectés sur votre réseau", "📱")

    if not reseau:
        print("  ❌ Impossible de détecter le réseau")
        return

    print("  ⏳ Scan en cours (10-20 secondes)...\n")

    base = ".".join(reseau.split(".")[:3])
    run(f"for i in $(seq 1 254); do ping -c1 -W1 {base}.$i & done; wait", timeout=25)

    arp = run("arp -a")
    appareils = []

    for ligne in arp.split("\n"):
        match = re.search(r"\((\d+\.\d+\.\d+\.\d+)\) at ([0-9a-f:]+)", ligne)
        if not match:
            continue
        ip_app = match.group(1)
        mac = match.group(2)
        if mac in ["ff:ff:ff:ff:ff:ff", "(incomplete)"]:
            continue

        try:
            hostname = socket.gethostbyaddr(ip_app)[0]
        except Exception:
            hostname = "Inconnu"

        fabricant = identifier_fabricant(mac)
        est_moi = ip_app == mon_ip
        appareils.append((ip_app, mac, hostname, fabricant, est_moi))

    if not appareils:
        print("  ℹ️  Aucun appareil détecté")
        return

    print(f"  {'IP':<18} {'MAC':<20} {'Fabricant':<20} {'Hostname'}")
    print(f"  {'─'*18} {'─'*20} {'─'*20} {'─'*20}")

    for ip_app, mac, hostname, fabricant, est_moi in sorted(appareils, key=lambda x: x[0]):
        flag = " 👈 VOUS" if est_moi else ""
        print(f"  {ip_app:<18} {mac:<20} {fabricant:<20} {hostname[:25]}{flag}")
        if est_moi:
            log("safe", "Appareil", f"{ip_app} → Votre Mac ✓")
        elif ip_app.startswith("224.") or ip_app.startswith("239."):
            log("safe", "Multicast", f"{ip_app} → Bonjour/mDNS Apple (normal) ✓")
        elif ip_app.startswith("192.168.64."):
            log("safe", "Virtuel", f"{ip_app} → Interface virtuelle macOS (normal) ✓")
        elif fabricant != "❓ Inconnu":
            log("safe", "Appareil", f"{ip_app} → {fabricant} ({hostname})")
        else:
            log("warning", "Appareil inconnu", f"{ip_app} ({mac}) — {hostname}")
            notifier_appareil_inconnu(ip_app, mac, hostname)

    print(f"\n  📊 Total : {len(appareils)} appareil(s) détecté(s)")

def identifier_fabricant(mac):
    """Identification locale par préfixe OUI."""
    prefixes = {
        "a4:c3:f0": "🍎 Apple", "f0:18:98": "🍎 Apple",
        "3c:22:fb": "🍎 Apple", "a8:be:27": "🍎 Apple",
        "00:17:f2": "🍎 Apple", "b8:27:eb": "🥧 Raspberry Pi",
        "dc:a6:32": "🥧 Raspberry Pi", "e4:5f:01": "🥧 Raspberry Pi",
        "00:50:f2": "💻 Microsoft", "28:d2:44": "📱 Samsung",
        "00:1a:11": "🔵 Google", "f4:f5:d8": "🔵 Google",
        "44:07:0b": "📦 Amazon", "fc:65:de": "📡 TP-Link",
        "50:c7:bf": "📡 TP-Link", "c8:3a:35": "📡 Tenda",
        "00:90:4c": "📡 Netgear", "20:e5:2a": "🎮 Nintendo",
        "98:b6:e9": "🎮 Nintendo",
    }
    mac_lower = mac.lower()
    for p, nom in prefixes.items():
        if mac_lower.startswith(p):
            return nom
    return "❓ Inconnu"

# ─────────────────────────────────────────
# 3. SCAN DE PORTS
# ─────────────────────────────────────────

def scanner_port(ip, port, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return port, True
    except Exception:
        return port, False

def scanner_ports(cibles):
    titre("Ports ouverts", "🔓")
    for cible in cibles:
        print(f"\n  🎯 Scan de {cible}...")
        ports_ouverts = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(scanner_port, cible, port): port for port in PORTS_COMMUNS}
            for future in as_completed(futures):
                port, ouvert = future.result()
                if ouvert:
                    ports_ouverts.append(port)
        if not ports_ouverts:
            log("safe", "Ports", f"{cible} → Aucun port sensible ouvert ✓")
        else:
            for port in sorted(ports_ouverts):
                service = PORTS_COMMUNS[port]
                if "⚠️" in service:
                    log("danger", "Port risqué", f"{cible}:{port} → {service}")
                elif port in [80, 8080]:
                    log("warning", "Port HTTP", f"{cible}:{port} → trafic non chiffré")
                else:
                    log("safe", "Port", f"{cible}:{port} → {service} ✓")

# ─────────────────────────────────────────
# 4. CONNEXIONS ACTIVES
# ─────────────────────────────────────────

def historique_connexions():
    titre("Connexions réseau actives par application", "📜")
    output = run("lsof -i -n -P 2>/dev/null | grep ESTABLISHED")
    if not output:
        log("safe", "Réseau", "Aucune connexion active détectée")
        return

    apps = {}
    for ligne in output.split("\n"):
        if not ligne.strip():
            continue
        parties = ligne.split()
        if len(parties) < 9:
            continue
        app = parties[0]
        adresse = parties[8] if len(parties) > 8 else "?"
        if app not in apps:
            apps[app] = []
        apps[app].append(adresse)

    apps_legit = [
        "firefox", "safari", "chrome", "claude", "slack", "discord",
        "spotify", "zoom", "teams", "dropbox", "1password", "notion",
        "code", "cursor", "python", "node", "git", "brew", "curl",
        "com.apple", "rapportd", "configd", "mDNSResponder", "sharingd"
    ]

    print(f"\n  {'Application':<20} {'Connexions':<12} {'Détail'}")
    print(f"  {'─'*20} {'─'*12} {'─'*30}")

    for app, conns in sorted(apps.items()):
        nb = len(conns)
        detail = conns[0][:40] if conns else ""
        est_legit = any(l in app.lower() for l in apps_legit)
        print(f"  {app:<20} {nb} sortantes    {detail}")
        if est_legit:
            log("safe", "App réseau", f"{app} → {nb} connexion(s) ✓")
        elif nb > 10:
            log("danger", "Trafic élevé", f"{app} → {nb} connexions simultanées !")
        else:
            log("warning", "App inconnue", f"{app} → {nb} connexion(s) — vérifiez")

# ─────────────────────────────────────────
# 5. RAPPORT FINAL
# ─────────────────────────────────────────

def rapport_final(ssid):
    titre("RAPPORT FINAL", "📊")

    nb_danger  = len(resultats["danger"])
    nb_warning = len(resultats["warning"])
    nb_safe    = len(resultats["safe"])

    if nb_danger == 0 and nb_warning <= 3:
        verdict = "🟢 Réseau sain — RAS"
        notif_msg = f"✅ Réseau sain sur {ssid}"
    elif nb_danger == 0:
        verdict = "🟡 Quelques points à vérifier"
        notif_msg = f"⚠️ {nb_warning} avertissements sur {ssid}"
    else:
        verdict = "🔴 Éléments critiques détectés !"
        notif_msg = f"🚨 {nb_danger} dangers sur {ssid} !"

    print(f"""
  🚨 Dangers      : {nb_danger}
  ⚠️  Avertissem. : {nb_warning}
  ✅ Safe         : {nb_safe}

  Verdict → {verdict}
    """)

    notifier("🌐 Network Analyzer", notif_msg)
    envoyer_rapport_complet()

    with open(RAPPORT_SORTIE, "w", encoding="utf-8") as f:
        f.write(f"🌐 Network Audit — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"Réseau : {ssid}\n")
        f.write("=" * 55 + "\n\n")
        for niveau in ["danger", "warning", "safe"]:
            if resultats[niveau]:
                label = {"danger": "🚨 DANGERS", "warning": "⚠️  AVERTISSEMENTS", "safe": "✅ SAFE"}[niveau]
                f.write(f"\n{label}\n{'─'*30}\n")
                for ligne in resultats[niveau]:
                    f.write(ligne + "\n")

    print(f"  📄 Rapport sauvegardé :\n  {RAPPORT_SORTIE}\n")

# ─────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("\n🌐 Network Analyzer — by Malone")
    print("=" * 55)
    print("  ⚠️  Utilisez uniquement sur votre propre réseau !\n")

    ip, reseau, gateway, interface = infos_reseau()
    ssid = obtenir_ssid(interface)
    scanner_appareils(reseau, ip)

    cibles = [c for c in [ip, gateway] if c]
    scanner_ports(cibles)

    historique_connexions()
    rapport_final(ssid)
