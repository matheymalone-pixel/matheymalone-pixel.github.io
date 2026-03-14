#!/Users/jessicacarrieredemonjeon/scripts/venv/bin/python3
"""
🛠️ Malone Tools — Menu Central
Lance tous vos scripts depuis un seul endroit.
Usage : tools
"""

import os
import time
from pathlib import Path

SCRIPTS_DIR = Path.home() / "scripts"
PYTHON = str(SCRIPTS_DIR) + "/venv/bin/python3"

OUTILS = [
    {
        "categorie": "🤖 Intelligence Artificielle",
        "couleur": "magenta",
        "outils": [
            {
                "nom":         "Assistant IA",
                "description": "Pose tes questions à Mistral en local",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/assistant.py",
                "alias":       "ai",
            },
        ]
    },
    {
        "categorie": "📁 Fichiers",
        "couleur": "cyan",
        "outils": [
            {
                "nom":         "Organisateur de Téléchargements",
                "description": "Trie automatiquement vos fichiers par catégorie",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/organiser_telechargements.py",
                'alias':       'trier',
	    },
	    {
                "nom":         "Dashboard Système",
                "description": "CPU, RAM, disque, batterie en temps réel",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/dashboard.py",
                "alias":       "dashboard",
         
            },
        ]
    },





    {
        'categorie': '🌤️ Météo & Utilitaires',
        'couleur': 'cyan',
        'outils': [
            {
                'nom':         'Météo locale',
                'description': 'Température, vent, prévisions 3 jours',
                'commande':    f'{PYTHON} {SCRIPTS_DIR}/meteo.py',
                'alias':       'meteo',
            },
	    {
                "nom":         "Pomodoro Timer",
                "description": "Timer 25min travail / 5min pause",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/pomodoro.py",
                "alias":       "pomodoro",
            },
	    {
                "nom":         "Journal de bord",
                "description": "Notes rapides depuis le terminal",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/journal.py",
                "alias":       "journal",
            },
        ]
    },
    {
        "categorie": "🔐 Sécurité",
        "couleur": "red",
        "outils": [
            {
                "nom":         "Audit de sécurité Mac",
                "description": "Scan fichiers suspects, processus, LaunchAgents",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/security_audit.py",
                "alias":       "audit",
            },
            {
                "nom":         "Analyseur réseau",
                "description": "Appareils WiFi, ports ouverts, connexions actives",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/network_analyzer.py",
                "alias":       "netaudit",
            },
            {
                "nom":         "Port Scanner Avancé",
                "description": "Scan ports, appareils réseau, détection dangers",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/port_scanner.py",
                "alias":       "portscan",
            },
            {
                "nom":         "Process Monitor",
                "description": "Surveille les processus suspects en temps réel",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/process_monitor.py",
                "alias":       "procmon",
            },
	    {
                "nom":         "Générateur de mots de passe",
                "description": "Génère des mots de passe forts et sécurisés",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/password_gen.py",
                "alias":       "passgen",
            },
	    {
                "nom":         "Traceroute Visuel",
                "description": "Trace le chemin d'un paquet sur internet",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/traceroute_visuel.py",
                "alias":       "traceroute-v",
            },
        ]
    },
    {
        "categorie": "🏗️ Développement",
        "couleur": "yellow",
        "outils": [
            {
                "nom":         "Générateur de projet",
                "description": "Crée une structure de projet Python en quelques secondes",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/newproject.py",
                "alias":       "newproject",
            },
        ]
    },
    {
        "categorie": "🎮 Projets",
        "couleur": "green",
        "outils": [
            {
                "nom":         "Re-Nature",
                "description": "Lance votre jeu pygame",
                "commande":    f"cd ~/Re-Nature/sources && {PYTHON} main.py",
                "alias":       "renature",
            },
         ]
     },
     {
        "categorie": "🎵 Musique",
        "couleur": "green",
        "outils": [
            {
                "nom":         "Spotify Controller",
                "description": "Contrôle Spotify depuis le terminal",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/spotify.py",
                "alias":       "spotify",
            },
            {
                "nom":         "ASCII Art",
                "description": "Convertit du texte en art ASCII stylé",
                "commande":    f"{PYTHON} {SCRIPTS_DIR}/ascii_art.py",
                "alias":       "ascii",
            },
        ]   
    },
]

# ─────────────────────────────────────────
# AFFICHAGE RICH
# ─────────────────────────────────────────

def afficher_menu():
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text
        from rich import box

        console = Console()
        os.system("clear")

        titre = Text("🛠️  Lemon 🍋 Tools v1.0", style="bold cyan", justify="center")
        console.print(Panel(titre, box=box.DOUBLE, border_style="cyan", padding=(0, 2)))
        console.print()

        index = 1
        mapping = {}

        for section in OUTILS:
            couleur = section["couleur"]
            console.print(f"  [{couleur}]{section['categorie']}[/{couleur}]")

            table = Table(
                box=box.ROUNDED,
                border_style=couleur,
                show_header=False,
                padding=(0, 1),
                expand=False,
            )
            table.add_column("N°",    style="bold white",  width=4)
            table.add_column("Nom",   style="bold white",  width=30)
            table.add_column("Description", style="dim white", width=42)
            table.add_column("Alias", style=f"bold {couleur}", width=12)

            for outil in section["outils"]:
                table.add_row(
                    f"[{couleur}]{index}[/{couleur}]",
                    outil["nom"],
                    outil["description"],
                    outil["alias"],
                )
                mapping[str(index)] = outil
                index += 1

            console.print(table)
            console.print()

        console.print("  [bold red][0][/bold red] Quitter\n")
        console.print("  " + "─" * 50)

        return mapping, console

    except ImportError:
        return afficher_menu_fallback()

# ─────────────────────────────────────────
# FALLBACK SANS RICH
# ─────────────────────────────────────────

def afficher_menu_fallback():
    os.system("clear")
    print("""
\033[1;36m  ╔══════════════════════════════════════╗
  ║        🛠️  Lemon 🍋 Tools v1.0         ║
  ╚══════════════════════════════════════╝\033[0m
    """)
    index = 1
    mapping = {}
    for section in OUTILS:
        print(f"\033[1;33m  {section['categorie']}\033[0m")
        print(f"  {'─'*38}")
        for outil in section["outils"]:
            print(f"  \033[1;37m[{index}]\033[0m {outil['nom']}")
            print(f"      \033[0;37m{outil['description']}\033[0m")
            print(f"      \033[0;35malias: {outil['alias']}\033[0m")
            print()
            mapping[str(index)] = outil
            index += 1
        print()
    print(f"  \033[1;31m[0]\033[0m Quitter")
    print(f"\n  {'─'*38}")
    return mapping, None

# ─────────────────────────────────────────
# LANCEMENT
# ─────────────────────────────────────────

def lancer_outil(outil, console=None):
    os.system("clear")

    if console:
        from rich.panel import Panel
        from rich.text import Text
        from rich import box
        titre = Text(f"🚀  {outil['nom']}", style="bold cyan")
        console.print(Panel(titre, box=box.ROUNDED, border_style="cyan", padding=(0, 2)))
        console.print()
    else:
        print(f"\n\033[1;36m  🚀 Lancement : {outil['nom']}\033[0m\n")
        print(f"  {'─'*38}\n")

    try:
        from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
        with Progress(
            TextColumn("  ⏳ [bold cyan]Chargement...[/bold cyan]"),
            BarColumn(bar_width=30),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task("", total=100)
            for i in range(100):
                time.sleep(0.015)
                progress.update(task, advance=1)
    except ImportError:
        pass

    print()
    os.system(outil["commande"])
    input("\n\n  ✅ Terminé — appuyez sur Entrée pour revenir au menu...")

# ─────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────
if __name__ == "__main__":
    try:
        import pyfiglet, time
        os.system("clear")
        print("\033[1;35m" + pyfiglet.figlet_format("Lemon", font="slant") + "\033[0m")
        print("\033[1;36m" + pyfiglet.figlet_format("Tools", font="slant") + "\033[0m")
        print("  \033[0;35m" + "-" * 45 + "\033[0m")
        print("  \033[0;35m  v1.0 - macOS . Python . Terminal\033[0m")
        print("  \033[0;35m" + "-" * 45 + "\033[0m")
        time.sleep(1.5)
    except:
        pass
    while True:
        result = afficher_menu()
        if isinstance(result, tuple):
            mapping, console = result
        else:
            mapping, console = result, None

        choix = input("\n  👉 Votre choix : ").strip()

        if choix == "0":
            os.system("clear")
            if console:
                console.print("\n  [bold cyan]👋 À bientôt Lemon ![/bold cyan]\n")
            else:
                print("\n  👋 À bientôt Lemon !\n")
            break
        elif choix in mapping:
            lancer_outil(mapping[choix], console)
        else:
            print("\n  ❌ Choix invalide, réessayez...")
            input("  Appuyez sur Entrée pour continuer...")
