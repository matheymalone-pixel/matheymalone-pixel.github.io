#!/usr/bin/env python3
"""
📝 Journal de bord — Lemon Tools
Notes rapides depuis le terminal, sauvegardées avec la date.
"""

import os
import json
from datetime import datetime
from pathlib import Path

JOURNAL_DIR = Path.home() / "scripts" / "journal"
JOURNAL_DIR.mkdir(exist_ok=True)

def run_notif(message):
    import subprocess
    subprocess.run(f'osascript -e \'display notification "{message}" with title "📝 Journal"\'',
                   shell=True, capture_output=True)

def get_fichier_jour():
    return JOURNAL_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.json"

def charger_notes():
    f = get_fichier_jour()
    if f.exists():
        with open(f) as file:
            return json.load(file)
    return []

def sauvegarder_notes(notes):
    with open(get_fichier_jour(), "w") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

def ajouter_note():
    print("\n  📝 Nouvelle note")
    print(f"  {'─'*40}")
    print("  (Entrée vide pour terminer)\n")

    lignes = []
    while True:
        ligne = input("  > ")
        if ligne == "":
            break
        lignes.append(ligne)

    if not lignes:
        print("  ❌ Note vide — annulé")
        return

    # Tag optionnel
    print("\n  🏷️  Tag (optionnel) : idée / todo / important / bug / autre")
    tag = input("  > ").strip().lower() or "note"

    note = {
        "id": datetime.now().strftime("%H%M%S"),
        "heure": datetime.now().strftime("%H:%M"),
        "tag": tag,
        "contenu": "\n".join(lignes),
    }

    notes = charger_notes()
    notes.append(note)
    sauvegarder_notes(notes)

    print(f"\n  \033[1;32m✅ Note sauvegardée !\033[0m")
    run_notif(f"Note ajoutée — {tag}")

def afficher_notes(notes, titre=""):
    reset = "\033[0m"
    tags_couleurs = {
        "idée":      "\033[1;35m",
        "todo":      "\033[1;33m",
        "important": "\033[1;31m",
        "bug":       "\033[1;31m",
        "note":      "\033[1;36m",
    }

    if titre:
        print(f"\n  {titre}")
    print(f"  {'─'*45}")

    if not notes:
        print("  📭 Aucune note")
        return

    for note in notes:
        couleur = tags_couleurs.get(note.get("tag", "note"), "\033[1;36m")
        tag = note.get("tag", "note").upper()
        heure = note.get("heure", "")
        contenu = note.get("contenu", "")

        print(f"\n  {couleur}[{tag}]\033[0m  🕐 {heure}")
        for ligne in contenu.splitlines():
            print(f"  {ligne}")

    print(f"\n  {'─'*45}")
    print(f"  📊 {len(notes)} note(s)")

def voir_aujourd_hui():
    notes = charger_notes()
    date = datetime.now().strftime("%d/%m/%Y")
    afficher_notes(notes, f"📅 Notes du {date}")

def voir_historique():
    fichiers = sorted(JOURNAL_DIR.glob("*.json"), reverse=True)
    if not fichiers:
        print("\n  📭 Aucun journal trouvé")
        return

    print(f"\n  📚 Historique du journal")
    print(f"  {'─'*40}")
    for i, f in enumerate(fichiers[:10], 1):
        date = f.stem
        with open(f) as file:
            notes = json.load(file)
        print(f"  [{i}] {date}  —  {len(notes)} note(s)")

    print(f"  {'─'*40}")
    choix = input("\n  👉 Voir quel jour ? (numéro ou Entrée pour retour) : ").strip()
    if choix.isdigit() and 1 <= int(choix) <= len(fichiers[:10]):
        f = fichiers[int(choix) - 1]
        with open(f) as file:
            notes = json.load(file)
        afficher_notes(notes, f"📅 {f.stem}")

def chercher_notes():
    mot = input("\n  🔍 Rechercher : ").strip().lower()
    if not mot:
        return

    fichiers = sorted(JOURNAL_DIR.glob("*.json"), reverse=True)
    resultats = []

    for f in fichiers:
        with open(f) as file:
            notes = json.load(file)
        for note in notes:
            if mot in note.get("contenu", "").lower() or mot in note.get("tag", "").lower():
                note["_date"] = f.stem
                resultats.append(note)

    print(f"\n  🔍 Résultats pour '{mot}'")
    print(f"  {'─'*40}")
    if not resultats:
        print(f"  ❌ Aucun résultat")
        return

    for note in resultats[:10]:
        print(f"\n  📅 {note.get('_date')}  🕐 {note.get('heure')}  [{note.get('tag','').upper()}]")
        for ligne in note.get("contenu", "").splitlines():
            print(f"  {ligne}")
    print(f"\n  📊 {len(resultats)} résultat(s)")

def supprimer_note():
    notes = charger_notes()
    if not notes:
        print("\n  📭 Aucune note aujourd'hui")
        return

    afficher_notes(notes, "📅 Notes d'aujourd'hui")
    print("\n  🗑️  Numéro de la note à supprimer (1, 2, 3...) :")
    choix = input("  > ").strip()

    if choix.isdigit() and 1 <= int(choix) <= len(notes):
        removed = notes.pop(int(choix) - 1)
        sauvegarder_notes(notes)
        print(f"  \033[1;32m✅ Note supprimée !\033[0m")
    else:
        print("  ❌ Numéro invalide")

def menu():
    os.system("clear")
    aujourd_hui = datetime.now().strftime("%d/%m/%Y")
    notes_today = charger_notes()

    print(f"\n\033[1;35m  📝  Journal de bord — Lemon Tools\033[0m")
    print(f"  \033[0;35m{'═' * 40}\033[0m")
    print(f"  📅 {aujourd_hui}  —  {len(notes_today)} note(s) aujourd'hui\n")
    print("  [1] Ajouter une note")
    print("  [2] Voir les notes d'aujourd'hui")
    print("  [3] Historique")
    print("  [4] Rechercher")
    print("  [5] Supprimer une note")
    print("  [0] Quitter")
    print(f"  \033[0;35m{'─' * 40}\033[0m")
    return input("\n  👉 Choix : ").strip()

def main():
    while True:
        choix = menu()

        if choix == "0":
            os.system("clear")
            break
        elif choix == "1":
            ajouter_note()
        elif choix == "2":
            voir_aujourd_hui()
        elif choix == "3":
            voir_historique()
        elif choix == "4":
            chercher_notes()
        elif choix == "5":
            supprimer_note()

        input("\n  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
