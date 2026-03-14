#!/usr/bin/env python3
"""
🎨 ASCII Art — Lemon Tools
Convertit du texte en art ASCII stylé.
"""

import os
import subprocess
from datetime import datetime

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout.strip()
    except:
        return ""

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "🎨 ASCII Art"\'')

try:
    import pyfiglet
except ImportError:
    print("❌ pyfiglet non installé")
    exit(1)

COULEURS = {
    "1": ("\033[1;35m", "Violet"),
    "2": ("\033[1;36m", "Cyan"),
    "3": ("\033[1;32m", "Vert"),
    "4": ("\033[1;31m", "Rouge"),
    "5": ("\033[1;33m", "Jaune"),
    "6": ("\033[1;37m", "Blanc"),
    "7": ("\033[1;34m", "Bleu"),
}

FONTS_POPULAIRES = [
    "big", "banner", "block", "bubble", "digital",
    "doom", "isometric1", "larry3d", "lean", "mini",
    "script", "shadow", "slant", "small", "speed",
    "standard", "star_wars", "stop", "thin", "3-d",
]

def afficher_art(texte, font, couleur_code):
    try:
        art = pyfiglet.figlet_format(texte, font=font)
        print(f"\n{couleur_code}{art}\033[0m")
        return art
    except Exception as e:
        print(f"\n  ❌ Erreur avec la police '{font}': {e}")
        return None

def sauvegarder_art(texte, art):
    nom = f"ascii_{texte[:10].replace(' ','_')}_{datetime.now().strftime('%H%M%S')}.txt"
    chemin = os.path.expanduser(f"~/Desktop/{nom}")
    with open(chemin, "w") as f:
        f.write(art)
    print(f"  \033[1;32m✅ Sauvegardé sur le Bureau : {nom}\033[0m")
    notifier(f"ASCII Art sauvegardé — {nom}")

def choisir_couleur():
    print("\n  🎨 Couleur :")
    for k, (_, nom) in COULEURS.items():
        code, _ = COULEURS[k]
        print(f"  [{k}] {code}{nom}\033[0m")
    choix = input("\n  👉 Couleur [1-7] : ").strip()
    return COULEURS.get(choix, COULEURS["1"])[0]

def menu():
    os.system("clear")
    print("\n\033[1;35m  🎨  ASCII Art — Lemon Tools\033[0m")
    print(f"  \033[0;35m{'═' * 42}\033[0m\n")
    print("  [1] Convertir du texte")
    print("  [2] Explorer les polices")
    print("  [3] Mode aléatoire — surprise !")
    print("  [4] Bannière Lemon Tools")
    print("  [0] Quitter")
    print(f"  \033[0;35m{'─' * 42}\033[0m")
    return input("\n  👉 Choix : ").strip()

def main():
    while True:
        choix = menu()

        if choix == "0":
            os.system("clear")
            break

        elif choix == "1":
            texte = input("\n  ✏️  Texte à convertir : ").strip()
            if not texte:
                continue

            print("\n  🔤 Polices disponibles :")
            for i, font in enumerate(FONTS_POPULAIRES, 1):
                print(f"  [{i:2}] {font}")

            font_choix = input("\n  👉 Numéro de police [1] : ").strip()
            try:
                font = FONTS_POPULAIRES[int(font_choix) - 1]
            except:
                font = "standard"

            couleur = choisir_couleur()
            art = afficher_art(texte, font, couleur)

            if art:
                save = input("\n  💾 Sauvegarder sur le Bureau ? [o/N] : ").strip().lower()
                if save == "o":
                    sauvegarder_art(texte, art)

        elif choix == "2":
            texte = input("\n  ✏️  Texte de test : ").strip() or "Lemon"
            couleur = choisir_couleur()
            print(f"\n  🔤 Aperçu de toutes les polices pour '{texte}' :\n")
            for font in FONTS_POPULAIRES:
                try:
                    art = pyfiglet.figlet_format(texte, font=font)
                    print(f"  \033[0;35m── {font} ──\033[0m")
                    print(f"{couleur}{art}\033[0m")
                except:
                    pass

        elif choix == "3":
            import random
            texte = input("\n  ✏️  Texte : ").strip() or "Lemon"
            font = random.choice(FONTS_POPULAIRES)
            couleur_key = str(random.randint(1, 7))
            couleur = COULEURS[couleur_key][0]
            print(f"\n  🎲 Police aléatoire : {font}")
            art = afficher_art(texte, font, couleur)
            if art:
                save = input("\n  💾 Sauvegarder ? [o/N] : ").strip().lower()
                if save == "o":
                    sauvegarder_art(texte, art)

        elif choix == "4":
            couleur = choisir_couleur()
            afficher_art("Lemon", "slant", couleur)
            afficher_art("Tools", "slant", "\033[1;36m")
            print(f"  \033[0;35m{'─' * 42}\033[0m")
            print(f"  \033[0;35mv1.0 — macOS · Python · Terminal\033[0m\n")

        input("\n  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
