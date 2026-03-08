PROJET MAC POUR AVOIR DES RACCOURCI :

-Avoir une version de python a jour ainsi que pip
-activer un venv



╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        🍋  Lemon Tools — by Lemon                        ║
║        macOS · Python · Terminal                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Un environnement de scripts Mac fait maison.
Audit sécurité · Analyse réseau · Assistant IA local · Organisateur de fichiers.


$ whoami
Développeur autodidacte passionné par l'automatisation, la sécurité et les outils en ligne de commande. Lemon Tools est mon environnement personnel — construit outil par outil, script par script.

$ ls ~/scripts/
ScriptDescriptionAliastools.pyMenu central — lance tous les scriptstoolsassistant.pyAssistant IA Mistral — 100% hors ligneaisecurity_audit.pyAudit sécurité Mac — fichiers, processus, LaunchAgentsauditnetwork_analyzer.pyAnalyse réseau — appareils, ports, connexionsnetauditorganiser_telechargements.pyTrie automatiquement les téléchargementstriernewproject.pyGénère une structure de projet Pythonnewprojectmenubar.pyIcône barre de menus Mac — accès sans terminal—

$ cat setup.txt
Terminal
├── iTerm2 + Thème Dracula
├── Oh My Zsh + Powerlevel10k
├── Plugins: zsh-autosuggestions, zsh-syntax-highlighting, fzf
└── Outils: eza, bat, zoxide

IA locale
├── Ollama
└── Mistral 7B — hors ligne, gratuit, privé

Automatisation (launchd)
├── com.malone.menubar       → barre de menus au démarrage
├── com.malone.ollama        → serveur Mistral au démarrage
└── com.malone.network-analyzer → analyse réseau au démarrage

VS Code
├── Dracula Official
├── Material Icon Theme
├── Python + Pylance + Black
├── GitLens + Error Lens
└── Live Server + Prettier

$ ./install.sh
bash# 1. Cloner le dépôt
git clone https://github.com/matheymalone-pixel/matheymalone-pixel.github.io.git

# 2. Créer l'environnement virtuel
cd scripts
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install rich textual rumps

# 4. Lancer le menu
python3 tools.py

$ netaudit --features
✅ Détection automatique du réseau actif (WiFi, iPhone hotspot, Ethernet)
✅ Scan des appareils connectés avec identification du fabricant
✅ Scan des ports ouverts (SSH, FTP, RDP, VNC...)
✅ Analyse des connexions actives par application
✅ Alertes email automatiques si appareil inconnu détecté
✅ Rapport complet envoyé par Gmail à chaque analyse
✅ Lancement automatique au démarrage via launchd

$ ai --info
Modèle   : Mistral 7B via Ollama
Connexion : aucune — 100% local
Coût     : 0€
Limite   : aucune
Langues  : français, anglais

$ git log --oneline
🍋 Launch Lemon Tools landing page
🤖 Ajout assistant IA Mistral local  
📧 Alertes email réseau automatiques
🎨 Refonte menu avec Rich + barre de progression
🔐 Amélioration security_audit — suppression faux positifs
🌐 Network analyzer — détection automatique du réseau
⚙️  Automatisation launchd au démarrage
🎨 Setup iTerm2 + Dracula + Powerlevel10k
🚀 Init — scripts réunis dans ~/scripts/


