#!/usr/bin/env python3
"""
🏗️ Générateur de structure de projet
Usage : python3 newproject.py
Auteur : Malone
"""

import os
import sys
from pathlib import Path

# ─────────────────────────────────────────
# 1. TEMPLATES DE PROJETS
# ─────────────────────────────────────────

TEMPLATES = {
    "1": {
        "nom": "🐍 Script Python simple",
        "description": "Un script standalone avec logs et config",
        "structure": {
            "main.py": '''#!/usr/bin/env python3
"""Point d\'entrée principal."""

def main():
    print("🚀 Projet lancé !")

if __name__ == "__main__":
    main()
''',
            "config.py": '''# ⚙️ Configuration du projet
DEBUG = True
VERSION = "1.0.0"
''',
            "requirements.txt": "# Ajoutez vos dépendances ici\n",
            ".gitignore": "__pycache__/\n*.pyc\n.env\n.DS_Store\nvenv/\n",
            "README.md": "# {nom_projet}\n\nDescription de votre projet.\n\n## Usage\n\n```bash\npython3 main.py\n```\n",
        }
    },
    "2": {
        "nom": "🌐 API Web (FastAPI)",
        "description": "Une API REST prête à l'emploi",
        "structure": {
            "main.py": '''#!/usr/bin/env python3
"""API FastAPI — Point d\'entrée."""
from fastapi import FastAPI

app = FastAPI(title="{nom_projet}", version="1.0.0")

@app.get("/")
def root():
    return {{"message": "🚀 API opérationnelle !"}}
''',
            "requirements.txt": "fastapi\nuvicorn\npydantic\n",
            ".env": "DEBUG=True\nPORT=8000\n",
            ".gitignore": "__pycache__/\n*.pyc\n.env\n.DS_Store\nvenv/\n",
            "README.md": "# {nom_projet}\n\n## Lancer l'API\n\n```bash\npip install -r requirements.txt\nuvicorn main:app --reload\n```\n",
            "routes/__init__.py": "",
            "routes/exemple.py": '''from fastapi import APIRouter
router = APIRouter()

@router.get("/exemple")
def exemple():
    return {{"data": "exemple"}}
''',
        }
    },
    "3": {
        "nom": "📊 Data Science",
        "description": "Analyse de données avec notebooks",
        "structure": {
            "main.py": '''#!/usr/bin/env python3
"""Analyse de données."""
import pandas as pd
import matplotlib.pyplot as plt

def charger_donnees(chemin: str) -> pd.DataFrame:
    return pd.read_csv(chemin)

def main():
    print("📊 Analyse prête !")

if __name__ == "__main__":
    main()
''',
            "requirements.txt": "pandas\nnumpy\nmatplotlib\nseaborn\njupyter\n",
            ".gitignore": "__pycache__/\n*.pyc\n.env\n.DS_Store\nvenv/\ndata/raw/\n",
            "README.md": "# {nom_projet}\n\n## Setup\n\n```bash\npip install -r requirements.txt\njupyter notebook\n```\n",
            "data/raw/.gitkeep": "",
            "data/processed/.gitkeep": "",
            "notebooks/analyse.ipynb": "",
            "src/__init__.py": "",
            "src/analyse.py": "# Fonctions d'analyse\n",
        }
    },
    "4": {
        "nom": "⚙️ Script d'automatisation",
        "description": "Outil CLI avec arguments et logs",
        "structure": {
            "main.py": '''#!/usr/bin/env python3
"""Script d\'automatisation avec CLI."""
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(message)s")
log = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="{nom_projet}")
    parser.add_argument("--verbose", action="store_true", help="Mode verbeux")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    log.info("🚀 Script lancé !")

if __name__ == "__main__":
    main()
''',
            "requirements.txt": "# Ajoutez vos dépendances ici\n",
            ".gitignore": "__pycache__/\n*.pyc\n.env\n.DS_Store\nvenv/\n",
            "README.md": "# {nom_projet}\n\n## Usage\n\n```bash\npython3 main.py --verbose\n```\n",
            "logs/.gitkeep": "",
        }
    },
}

# ─────────────────────────────────────────
# 2. AFFICHAGE DU MENU
# ─────────────────────────────────────────

def afficher_menu():
    print("\n🏗️  Générateur de Projet Python")
    print("─" * 40)
    for key, template in TEMPLATES.items():
        print(f"  {key}. {template['nom']}")
        print(f"     {template['description']}")
    print("─" * 40)

# ─────────────────────────────────────────
# 3. CRÉATION DE LA STRUCTURE
# ─────────────────────────────────────────

def creer_projet(nom_projet: str, template: dict):
    dossier_base = Path.cwd() / nom_projet

    if dossier_base.exists():
        print(f"❌ Le dossier '{nom_projet}' existe déjà !")
        sys.exit(1)

    print(f"\n📁 Création de '{nom_projet}'...\n")

    for chemin_relatif, contenu in template["structure"].items():
        # Remplace {nom_projet} dans le contenu
        contenu_final = contenu.replace("{nom_projet}", nom_projet)
        chemin_complet = dossier_base / chemin_relatif

        # Crée les dossiers parents si nécessaire
        chemin_complet.parent.mkdir(parents=True, exist_ok=True)

        # Crée le fichier
        chemin_complet.write_text(contenu_final, encoding="utf-8")
        print(f"  ✅ {chemin_relatif}")

    print(f"\n🎉 Projet '{nom_projet}' créé avec succès !")
    print(f"\n👉 Pour démarrer :\n")
    print(f"   cd {nom_projet}")
    print(f"   python3 -m venv venv")
    print(f"   source venv/bin/activate")
    print(f"   pip install -r requirements.txt")
    print(f"   python3 main.py\n")

# ─────────────────────────────────────────
# 4. POINT D'ENTRÉE
# ─────────────────────────────────────────

if __name__ == "__main__":
    afficher_menu()

    choix = input("👉 Choisissez un template (1-4) : ").strip()
    if choix not in TEMPLATES:
        print("❌ Choix invalide !")
        sys.exit(1)

    nom = input("📝 Nom du projet : ").strip().lower().replace(" ", "_")
    if not nom:
        print("❌ Nom invalide !")
        sys.exit(1)

    creer_projet(nom, TEMPLATES[choix])
