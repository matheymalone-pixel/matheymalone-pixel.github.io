#!/usr/bin/env python3
"""
🔑 Générateur de mots de passe — Lemon Tools
Génère des mots de passe forts et sécurisés.
"""

import secrets
import string
import subprocess
import os
from datetime import datetime

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout.strip()
    except:
        return ""

def copier_presse_papier(texte):
    subprocess.run("pbcopy", input=texte.encode(), check=True)

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "🔑 Mot de passe"\'')

def force_mdp(mdp):
    score = 0
    if len(mdp) >= 8:   score += 1
    if len(mdp) >= 16:  score += 1
    if any(c.isupper() for c in mdp): score += 1
    if any(c.islower() for c in mdp): score += 1
    if any(c.isdigit() for c in mdp): score += 1
    if any(c in string.punctuation for c in mdp): score += 1

    if score <= 2:   return "Faible",   "\033[1;31m", "██░░░░░░░░"
    elif score <= 4: return "Moyen",    "\033[1;33m", "█████░░░░░"
    else:            return "Fort 💪",  "\033[1;32m", "██████████"

def generer_simple():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(chars) for _ in range(12))

def generer_long():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return "".join(secrets.choice(chars) for _ in range(24))

def generer_passphrase():
    mots = [
        "cheval", "montagne", "soleil", "rivière", "forêt", "nuage", "étoile",
        "pierre", "feuille", "oiseau", "lumière", "ombre", "océan", "désert",
        "cascade", "tonnerre", "brume", "cristal", "flamme", "glacier",
        "lemon", "python", "terminal", "clavier", "écran", "serveur",
    ]
    selection = [secrets.choice(mots) for _ in range(4)]
    nombre = secrets.randbelow(99) + 1
    return f"{'-'.join(selection)}-{nombre}"

def generer_pin(longueur=6):
    return "".join([str(secrets.randbelow(10)) for _ in range(longueur)])

def generer_custom(longueur, majuscules, chiffres, symboles):
    chars = string.ascii_lowercase
    if majuscules: chars += string.ascii_uppercase
    if chiffres:   chars += string.digits
    if symboles:   chars += "!@#$%^&*()-_=+"
    return "".join(secrets.choice(chars) for _ in range(longueur))

def afficher_mdp(mdp, label=""):
    force, couleur, barre = force_mdp(mdp)
    reset = "\033[0m"
    print(f"\n  {'─'*45}")
    if label:
        print(f"  📋 {label}")
    print(f"  🔑 \033[1;37m{mdp}\033[0m")
    print(f"  💪 Force : {couleur}{barre} {force}{reset}")
    print(f"  📏 Longueur : {len(mdp)} caractères")
    print(f"  {'─'*45}")

    copier = input("\n  📋 Copier dans le presse-papier ? [O/n] : ").strip().lower()
    if copier != "n":
        copier_presse_papier(mdp)
        print(f"  \033[1;32m✅ Copié !\033[0m")
        notifier("✅ Mot de passe copié dans le presse-papier")

def menu():
    os.system("clear")
    print("\n🔑  Générateur de mots de passe — Lemon Tools")
    print("=" * 48)
    print(f"  🕐 {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
    print("  [1] Mot de passe simple     12 caractères")
    print("  [2] Mot de passe long       24 caractères")
    print("  [3] Passphrase              4 mots + nombre")
    print("  [4] PIN                     6 chiffres")
    print("  [5] Personnalisé            longueur au choix")
    print("  [6] Générer plusieurs       lot de mots de passe")
    print("  [0] Quitter")
    print(f"  {'─'*48}")
    return input("\n  👉 Choix : ").strip()

def main():
    while True:
        choix = menu()

        if choix == "0":
            os.system("clear")
            break

        elif choix == "1":
            mdp = generer_simple()
            afficher_mdp(mdp, "Mot de passe simple")

        elif choix == "2":
            mdp = generer_long()
            afficher_mdp(mdp, "Mot de passe long")

        elif choix == "3":
            mdp = generer_passphrase()
            afficher_mdp(mdp, "Passphrase")

        elif choix == "4":
            longueur = input("\n  📏 Longueur du PIN [6] : ").strip()
            longueur = int(longueur) if longueur.isdigit() else 6
            mdp = generer_pin(longueur)
            afficher_mdp(mdp, f"PIN {longueur} chiffres")

        elif choix == "5":
            longueur = input("\n  📏 Longueur : ").strip()
            longueur = int(longueur) if longueur.isdigit() else 16
            maj = input("  🔠 Majuscules ? [O/n] : ").strip().lower() != "n"
            chif = input("  🔢 Chiffres ? [O/n] : ").strip().lower() != "n"
            symb = input("  ⚡ Symboles ? [O/n] : ").strip().lower() != "n"
            mdp = generer_custom(longueur, maj, chif, symb)
            afficher_mdp(mdp, "Mot de passe personnalisé")

        elif choix == "6":
            nb = input("\n  🔢 Combien de mots de passe ? [5] : ").strip()
            nb = int(nb) if nb.isdigit() else 5
            print(f"\n  {'─'*45}")
            print(f"  {'#':<4} {'MOT DE PASSE':<28} FORCE")
            print(f"  {'─'*45}")
            reset = "\033[0m"
            for i in range(1, nb + 1):
                mdp = generer_long()
                force, couleur, _ = force_mdp(mdp)
                print(f"  {i:<4} \033[1;37m{mdp:<28}\033[0m {couleur}{force}{reset}")
            print(f"  {'─'*45}")

        input("\n  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
