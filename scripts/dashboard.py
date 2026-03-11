#!/usr/bin/env python3
"""
📊 Dashboard Système — Lemon Tools
Affiche CPU, RAM, disque, température et batterie en temps réel.
"""

import subprocess
import os
import time
from datetime import datetime

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""

def barre(pct, largeur=20):
    filled = int(largeur * pct / 100)
    empty = largeur - filled
    if pct >= 80:   couleur = "\033[1;31m"
    elif pct >= 60: couleur = "\033[1;33m"
    else:           couleur = "\033[1;32m"
    reset = "\033[0m"
    return f"{couleur}{'█' * filled}{'░' * empty}{reset}"

def get_cpu():
    result = run("top -l 1 -n 0 | grep 'CPU usage'")
    try:
        user = float(result.split()[2].replace("%", ""))
        sys  = float(result.split()[4].replace("%", ""))
        return round(user + sys, 1)
    except:
        return 0.0

def get_ram():
    result = run("vm_stat")
    try:
        lines = result.splitlines()
        stats = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":")
                stats[k.strip()] = int(v.strip().replace(".", ""))
        page = 4096
        active   = stats.get("Pages active", 0) * page
        inactive = stats.get("Pages inactive", 0) * page
        wired    = stats.get("Pages wired down", 0) * page
        free     = stats.get("Pages free", 0) * page
        used = active + inactive + wired
        total = used + free
        pct = round(used / total * 100) if total > 0 else 0
        return round(used / 1024**3, 1), round(total / 1024**3, 1), pct
    except:
        return 0, 0, 0

def get_disque():
    result = run("df -H / | tail -1")
    try:
        parts = result.split()
        total = parts[1]
        used  = parts[2]
        pct   = int(parts[4].replace("%", ""))
        return used, total, pct
    except:
        return "?", "?", 0

def get_batterie():
    result = run("pmset -g batt")
    try:
        lines = result.splitlines()
        for line in lines:
            if "%" in line:
                pct = int(line.split("%")[0].split()[-1])
                charge = "⚡ En charge" if "charging" in line.lower() else "🔋 Sur batterie" if "discharging" in line.lower() else "✅ Chargé"
                return pct, charge
    except:
        pass
    return None, None

def get_temp():
    result = run("sudo powermetrics -n 1 -i 1 --samplers smc 2>/dev/null | grep 'CPU die temperature'")
    try:
        return float(result.split(":")[1].strip().replace("C", "").strip())
    except:
        # Fallback sans sudo
        result2 = run("osx-cpu-temp 2>/dev/null")
        try:
            return float(result2.replace("°C", "").strip())
        except:
            return None

def get_uptime():
    result = run("uptime | awk '{print $3, $4}' | sed 's/,//'")
    return result if result else "?"

def get_processus_top():
    result = run("ps aux | sort -rk 3 | head -6 | tail -5")
    procs = []
    for line in result.splitlines():
        parts = line.split()
        if len(parts) >= 11:
            try:
                nom = os.path.basename(parts[10])[:20]
                cpu = float(parts[2])
                procs.append((nom, cpu))
            except:
                pass
    return procs

def afficher_dashboard():
    os.system("clear")
    now = datetime.now().strftime('%d/%m/%Y à %H:%M:%S')
    reset = "\033[0m"

    print(f"\n\033[1;35m  📊  Dashboard Système — Lemon Tools\033[0m")
    print(f"  \033[0;35m{'═' * 48}\033[0m")
    print(f"  🕐 {now}     ⏱️  Uptime: {get_uptime()}")
    print(f"  {'─' * 48}")

    # CPU
    cpu = get_cpu()
    print(f"\n  🖥️  CPU")
    print(f"  {barre(cpu)}  \033[1;37m{cpu}%\033[0m")

    # RAM
    ram_used, ram_total, ram_pct = get_ram()
    print(f"\n  💾  RAM")
    print(f"  {barre(ram_pct)}  \033[1;37m{ram_pct}%\033[0m   {ram_used}GB / {ram_total}GB")

    # Disque
    disk_used, disk_total, disk_pct = get_disque()
    print(f"\n  💿  Disque")
    print(f"  {barre(disk_pct)}  \033[1;37m{disk_pct}%\033[0m   {disk_used} / {disk_total}")

    # Batterie
    batt_pct, batt_status = get_batterie()
    if batt_pct is not None:
        print(f"\n  🔋  Batterie")
        print(f"  {barre(batt_pct)}  \033[1;37m{batt_pct}%\033[0m   {batt_status}")

    # Température
    temp = get_temp()
    if temp:
        if temp >= 80:   tc = "\033[1;31m"
        elif temp >= 60: tc = "\033[1;33m"
        else:            tc = "\033[1;32m"
        print(f"\n  🌡️  Température CPU : {tc}{temp}°C{reset}")

    # Top processus CPU
    procs = get_processus_top()
    if procs:
        print(f"\n  {'─' * 48}")
        print(f"  🔥  Top processus CPU")
        for nom, cpu_p in procs:
            bar = barre(min(cpu_p * 2, 100), 12)
            print(f"  {bar}  {cpu_p:>5.1f}%  {nom}")

    print(f"\n  {'─' * 48}")
    print(f"  \033[0;35m[R] Rafraîchir   [Q] Quitter\033[0m")

def main():
    print("\n  ⏳ Chargement du dashboard...")
    while True:
        afficher_dashboard()
        choix = input("\n  👉 ").strip().upper()
        if choix == "Q":
            os.system("clear")
            break
        # R ou Entrée = rafraîchir

if __name__ == "__main__":
    main()
