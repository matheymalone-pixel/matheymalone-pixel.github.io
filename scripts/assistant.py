#!/usr/bin/env python3
"""
🤖 Assistant IA — Malone Tools
Propulsé par Mistral via Ollama
"""

import subprocess
import os

def chat(message, historique=[]):
    """Envoie un message à Mistral."""
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", message],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        return f"❌ Erreur : {e}"

def main():
    os.system("clear")
    print("""
\033[1;36m  ╔══════════════════════════════════════╗
  ║        🤖 Assistant Malone           ║
  ║        Propulsé par Mistral          ║
  ╚══════════════════════════════════════╝\033[0m

  \033[0;37mTape 'exit' pour quitter\033[0m
  \033[0;37mTape 'clear' pour effacer\033[0m
    """)

    while True:
        try:
            question = input("\n  \033[1;36m Vous\033[0m : ").strip()
        except KeyboardInterrupt:
            print("\n\n  👋 À bientôt !\n")
            break

        if not question:
            continue
        if question.lower() == "exit":
            print("\n  👋 À bientôt !\n")
            break
        if question.lower() == "clear":
            os.system("clear")
            continue

        print("\n  \033[1;35m🤖 Mistral\033[0m : ", end="", flush=True)
        reponse = chat(question)
        print(reponse)

if __name__ == "__main__":
    main()
