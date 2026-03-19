#!/usr/bin/env python3
"""
📝 Résumé de page web — Lemon Tools
Résume n'importe quel article avec Mistral en local.
"""

import subprocess
import json
import os
import re
from datetime import datetime

def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""

def notifier(message):
    run(f'osascript -e \'display notification "{message}" with title "📝 Résumé Web"\'')

def extraire_texte(url):
    # Télécharge la page
    html = run(f'curl -s --max-time 15 -L "{url}" 2>/dev/null')
    if not html:
        return None

    # Supprime les balises HTML
    texte = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    texte = re.sub(r'<style[^>]*>.*?</style>', '', texte, flags=re.DOTALL)
    texte = re.sub(r'<[^>]+>', ' ', texte)
    texte = re.sub(r'\s+', ' ', texte)
    texte = texte.strip()

    # Limite à 3000 caractères pour Mistral
    return texte[:3000] if texte else None

def resumer_avec_mistral(texte, url):
    prompt = f"""Tu es un assistant qui résume des articles web en français de manière claire et concise.

Voici le contenu d'une page web ({url}) :

{texte}

Fais un résumé en français en 5-8 phrases. Inclus :
- Le sujet principal
- Les points clés
- La conclusion

Résumé :"""
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "60", "-X", "POST",
             "http://localhost:11434/api/generate",
             "-H", "Content-Type: application/json",
             "-d", json.dumps({"model": "mistral", "prompt": prompt, "stream": False})],
            capture_output=True, text=True, timeout=65
        )
        data = json.loads(result.stdout)
        return data.get("response", "").strip()
    except:
        return None

def sauvegarder_resume(url, resume):
    nom = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    chemin = os.path.expanduser(f"~/Desktop/{nom}")
    with open(chemin, "w") as f:
        f.write(f"URL : {url}\n")
        f.write(f"Date : {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
        f.write(f"{'─'*50}\n\n")
        f.write(resume)
    print(f"\n  \033[1;32m✅ Sauvegardé sur le Bureau : {nom}\033[0m")
    notifier(f"Résumé sauvegardé — {nom}")

def menu():
    os.system("clear")
    print("\n\033[1;35m  📝  Résumé de page web — Lemon Tools\033[0m")
    print(f"  \033[0;35m{'═' * 45}\033[0m\n")
    print("  🤖 Propulsé par Mistral en local\n")
    print("  [1] Résumer une page web")
    print("  [2] Résumer plusieurs pages")
    print("  [0] Quitter")
    print(f"  \033[0;35m{'─' * 45}\033[0m")
    return input("\n  👉 Choix : ").strip()

def traiter_url(url):
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\n  ⏳ Téléchargement de {url}...")
    texte = extraire_texte(url)

    if not texte or len(texte) < 100:
        print("  ❌ Impossible d'extraire le contenu")
        print("  💡 Vérifiez l'URL ou essayez un autre article")
        return

    print(f"  ✅ {len(texte)} caractères extraits")
    print(f"  🤖 Mistral analyse en cours...\n")

    resume = resumer_avec_mistral(texte, url)

    if not resume:
        print("  ❌ Mistral n'est pas disponible")
        print("  💡 Vérifiez qu'Ollama tourne : ollama serve")
        return

    print(f"  \033[1;36m{'─'*45}\033[0m")
    print(f"  📝 RÉSUMÉ\n")
    print(f"  {resume}\n")
    print(f"  \033[1;36m{'─'*45}\033[0m")

    save = input("\n  💾 Sauvegarder sur le Bureau ? [o/N] : ").strip().lower()
    if save == "o":
        sauvegarder_resume(url, resume)

    notifier("✅ Résumé terminé !")

def main():
    # Vérifier Ollama
    check = run("curl -s http://localhost:11434/api/tags --max-time 3")
    if not check:
        print("\n  ❌ Ollama n'est pas lancé !")
        print("  💡 Lance : ollama serve")
        input("\n  Appuyez sur Entrée...")
        return

    while True:
        choix = menu()

        if choix == "0":
            os.system("clear")
            break

        elif choix == "1":
            url = input("\n  🌐 URL de l'article : ").strip()
            if url:
                traiter_url(url)

        elif choix == "2":
            print("\n  🌐 Entre les URLs (une par ligne, ligne vide pour terminer) :")
            urls = []
            while True:
                url = input("  > ").strip()
                if not url:
                    break
                urls.append(url)

            for i, url in enumerate(urls, 1):
                print(f"\n  {'─'*45}")
                print(f"  📰 Article {i}/{len(urls)}")
                traiter_url(url)

        input("\n\n  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
