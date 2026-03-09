#!/usr/bin/env python3
"""
🗂️ Organisateur de Téléchargements — Mac
Trie automatiquement vos fichiers par catégorie.
Auteur : Malone | Usage : python3 organiser_telechargements.py
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────
# 1. CONFIGURATION — adaptez à votre goût
# ─────────────────────────────────────────

DOSSIER_SOURCE = Path.home() / "Downloads"

CATEGORIES = {
    "📄 Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "🖼️ Images":    [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp"],
    "🎬 Vidéos":    [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".m4v"],
    "🗜️ Archives":  [".zip", ".rar", ".tar", ".gz", ".dmg", ".pkg", ".iso"],
    "🐍 Scripts":   [".py", ".sh", ".js", ".ts", ".rb", ".php", ".html", ".css"],
    "🎵 Audio":     [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg"],
}

# ─────────────────────────────────────────
# 2. CRÉATION DES DOSSIERS
# ─────────────────────────────────────────

def creer_dossiers():
    for nom_dossier in CATEGORIES:
        chemin = DOSSIER_SOURCE / nom_dossier
        chemin.mkdir(exist_ok=True)
    # Dossier pour tout ce qui ne correspond à rien
    (DOSSIER_SOURCE / "📦 Autres").mkdir(exist_ok=True)
    print("✅ Dossiers créés")

# ─────────────────────────────────────────
# 3. TRI DES FICHIERS
# ─────────────────────────────────────────

def trouver_categorie(extension):
    """Retourne le nom du dossier cible selon l'extension."""
    for categorie, extensions in CATEGORIES.items():
        if extension.lower() in extensions:
            return categorie
    return "📦 Autres"

def eviter_ecrasement(destination):
    """Si un fichier du même nom existe déjà, ajoute un timestamp."""
    if not destination.exists():
        return destination
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return destination.with_stem(f"{destination.stem}_{timestamp}")

def trier_fichiers():
    fichiers = [f for f in DOSSIER_SOURCE.iterdir() if f.is_file()]
    
    if not fichiers:
        print("📂 Aucun fichier à trier !")
        return

    deplacés = 0
    ignorés  = 0

    print(f"\n🔍 {len(fichiers)} fichier(s) trouvé(s)...\n")

    for fichier in fichiers:
        # On ignore les fichiers cachés (.DS_Store, etc.)
        if fichier.name.startswith("."):
            ignorés += 1
            continue

        categorie   = trouver_categorie(fichier.suffix)
        destination = eviter_ecrasement(DOSSIER_SOURCE / categorie / fichier.name)

        shutil.move(str(fichier), str(destination))
        print(f"  {fichier.name:40} →  {categorie}")
        deplacés += 1

    print(f"\n✅ Terminé ! {deplacés} fichier(s) trié(s), {ignorés} ignoré(s).")

# ─────────────────────────────────────────
# 4. POINT D'ENTRÉE
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("🗂️  Organisateur de Téléchargements\n" + "─" * 40)
    creer_dossiers()
    trier_fichiers()
