# 🎥 Extracteur d'Idées YouTube

Application Streamlit qui extrait la transcription d'une vidéo YouTube et utilise l'IA d'OpenAI pour analyser et résumer les idées principales.

## 🚀 Fonctionnalités

- ✅ Extraction automatique de la transcription YouTube
- 🤖 Analyse intelligente avec GPT-4
- 📊 Résumé structuré des idées principales
- 💾 Téléchargement de l'analyse
- 🌍 Support multilingue (français et anglais)

## 📋 Prérequis

- Python 3.8+
- Une clé API OpenAI
- Un compte GitHub (pour le déploiement)
- Un compte Streamlit Cloud (gratuit)

## 🛠️ Installation locale

1. **Cloner le projet**
```bash
git clone https://github.com/votre-username/votre-repo.git
cd votre-repo
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer la clé API**
   - Créer le dossier `.streamlit` s'il n'existe pas
   - Ouvrir le fichier `.streamlit/secrets.toml`
   - Remplacer `"votre-clé-api-ici"` par votre vraie clé OpenAI

4. **Lancer l'application**
```bash
streamlit run app.py
```

## ☁️ Déploiement sur Streamlit Cloud

### Étape 1 : Préparer GitHub

1. **Créer un nouveau dépôt sur GitHub** (public ou privé)

2. **Pousser votre code sur GitHub**
```bash
git init
git add app.py requirements.txt .gitignore README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/votre-username/votre-repo.git
git push -u origin main
```

⚠️ **IMPORTANT** : Ne JAMAIS commiter le fichier `.streamlit/secrets.toml` !

### Étape 2 : Déployer sur Streamlit Cloud

1. **Aller sur** [share.streamlit.io](https://share.streamlit.io)

2. **Se connecter** avec votre compte GitHub

3. **Cliquer sur "New app"**

4. **Configurer l'application :**
   - Repository : sélectionner votre dépôt
   - Branch : main
   - Main file path : app.py

5. **Ajouter la clé API (CRUCIAL) :**
   - Cliquer sur "Advanced settings"
   - Dans la section "Secrets", ajouter :
   ```toml
   OPENAI_API_KEY = "sk-votre-clé-openai-réelle"
   ```

6. **Cliquer sur "Deploy"**

🎉 Votre application sera accessible à tous via l'URL fournie, et votre clé API restera sécurisée !

## 🔐 Sécurité de la clé API

### Comment ça fonctionne ?

1. **Localement** : La clé est dans `.streamlit/secrets.toml` (ignoré par Git)
2. **Sur Streamlit Cloud** : La clé est dans les "Secrets" de l'application
3. **Dans le code** : On utilise `st.secrets["OPENAI_API_KEY"]`

### Avantages :
- ✅ La clé n'apparaît JAMAIS dans le code sur GitHub
- ✅ La clé est utilisée pour tous les utilisateurs de l'app
- ✅ Vous seul pouvez voir/modifier la clé dans les paramètres Streamlit Cloud
- ✅ Les utilisateurs bénéficient de l'IA sans avoir besoin de leur propre clé

## 📖 Utilisation

1. Coller l'URL d'une vidéo YouTube (qui a des sous-titres)
2. Cliquer sur "Analyser la vidéo"
3. Consulter la transcription et l'analyse IA
4. Télécharger les résultats si besoin

## 🔧 Formats d'URL supportés

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## ⚠️ Limitations

- La vidéo doit avoir des sous-titres disponibles (générés automatiquement ou manuels)
- La transcription est limitée à ~15 000 caractères pour l'analyse IA (pour respecter les limites de tokens)

## 🆘 Dépannage

**Erreur "Clé API non configurée"**
- Sur Streamlit Cloud : Vérifier que la clé est bien dans les Secrets
- En local : Vérifier que `.streamlit/secrets.toml` contient votre clé

**Erreur "Aucune transcription disponible"**
- La vidéo n'a pas de sous-titres activés
- Essayer une autre vidéo

**Erreur lors de l'analyse**
- Vérifier que votre clé OpenAI est valide
- Vérifier que vous avez du crédit sur votre compte OpenAI

## 📝 Licence

Libre d'utilisation pour vos projets personnels et professionnels.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.